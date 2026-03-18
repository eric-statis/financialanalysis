#!/usr/bin/env python3
"""
将结构化知识增量直接写入正式 knowledge_base.json，并记录 adoption log。
"""

import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from runtime_support import RuntimeConfigError, load_runtime_config, resolve_runtime_path


def now_iso() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str) -> str:
    text = "".join(ch if ch.isalnum() else "_" for ch in str(value or "").strip())
    text = text.strip("_")
    return text or "unknown"


def read_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)



def write_json(path: Path, payload: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    temp_path.replace(path)



def md5_payload(payload: Dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.md5(encoded).hexdigest()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="写入正式 knowledge_base 并记录 adoption log")
    parser.add_argument("--delta", required=True, help="结构化增量 JSON 路径")
    parser.add_argument("--runtime-config", help="显式指定 runtime/runtime_config.json")
    return parser.parse_args()



def resolve_parent_and_key(root: Dict[str, Any], path_text: str, *, create_missing: bool) -> Tuple[Any, str]:
    parts = [part for part in path_text.split(".") if part]
    if not parts:
        raise SystemExit("operation.path 不能为空")

    current: Any = root
    for part in parts[:-1]:
        if isinstance(current, dict):
            if part not in current:
                if not create_missing:
                    raise SystemExit(f"路径不存在: {path_text}")
                current[part] = {}
            current = current[part]
            continue
        raise SystemExit(f"路径中间节点不是对象: {path_text}")
    return current, parts[-1]



def apply_operation(payload: Dict[str, Any], operation: Dict[str, Any]):
    op = str(operation.get("op", "")).strip()
    path_text = str(operation.get("path", "")).strip()
    if op not in {"set", "append", "upsert_by_key"}:
        raise SystemExit(f"不支持的操作: {op}")
    if not path_text:
        raise SystemExit("operation.path 缺失")

    parent, key = resolve_parent_and_key(payload, path_text, create_missing=True)

    if op == "set":
        if not isinstance(parent, dict):
            raise SystemExit(f"set 目标父节点必须是对象: {path_text}")
        parent[key] = operation.get("value")
        return

    if not isinstance(parent, dict):
        raise SystemExit(f"{op} 目标父节点必须是对象: {path_text}")

    if key not in parent:
        parent[key] = []
    target = parent[key]
    if not isinstance(target, list):
        raise SystemExit(f"{op} 目标必须是列表: {path_text}")

    if op == "append":
        target.append(operation.get("value"))
        return

    match_key = str(operation.get("match_key", "")).strip()
    match_value = operation.get("match_value")
    value = operation.get("value")
    if not match_key:
        raise SystemExit("upsert_by_key 缺少 match_key")
    if not isinstance(value, dict):
        raise SystemExit("upsert_by_key 的 value 必须是对象")

    for index, item in enumerate(target):
        if isinstance(item, dict) and item.get(match_key) == match_value:
            merged = dict(item)
            merged.update(value)
            target[index] = merged
            return
    target.append(value)



def main():
    args = parse_args()
    delta_path = Path(args.delta).resolve()
    if not delta_path.exists():
        raise SystemExit(f"delta 文件不存在: {delta_path}")

    try:
        runtime_config = load_runtime_config(
            config_path=Path(args.runtime_config) if args.runtime_config else None,
            cwd=Path.cwd(),
            require_knowledge_base=True,
            ensure_state_dirs=True,
        )
    except RuntimeConfigError as exc:
        raise SystemExit(str(exc)) from exc

    delta_payload = read_json(delta_path)
    operations = delta_payload.get("operations")
    if not isinstance(operations, list) or not operations:
        raise SystemExit("delta.operations 必须是非空列表")

    knowledge_base_path = resolve_runtime_path(runtime_config, "knowledge_base")
    adoption_log_dir = resolve_runtime_path(runtime_config, "knowledge_adoption_log_dir")
    knowledge_base = read_json(knowledge_base_path)
    before_payload = copy.deepcopy(knowledge_base)
    before_hash = md5_payload(before_payload)

    for operation in operations:
        if not isinstance(operation, dict):
            raise SystemExit("operations 中每项必须是对象")
        apply_operation(knowledge_base, operation)

    metadata = knowledge_base.setdefault("metadata", {})
    metadata["last_updated"] = datetime.date.today().isoformat()
    after_hash = md5_payload(knowledge_base)

    source = delta_payload.get("source") or {}
    case_name = slugify(source.get("case_name") or source.get("issuer") or delta_payload.get("case_name", "case"))
    chapter_no = source.get("chapter_no", "unknown")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{timestamp}_{case_name}_chapter_{chapter_no}"
    backup_path = adoption_log_dir / f"{base_name}.before.json"
    log_path = adoption_log_dir / f"{base_name}.log.json"

    write_json(backup_path, before_payload)
    write_json(knowledge_base_path, knowledge_base)
    write_json(
        log_path,
        {
            "logged_at": now_iso(),
            "delta_path": str(delta_path),
            "knowledge_base_path": str(knowledge_base_path),
            "backup_path": str(backup_path),
            "before_hash": before_hash,
            "after_hash": after_hash,
            "source": source,
            "summary": delta_payload.get("summary", ""),
            "operations": operations,
        },
    )

    print(f"[OK] knowledge_base: {knowledge_base_path}")
    print(f"[OK] adoption_log: {log_path}")
    print(f"[OK] before_hash={before_hash} after_hash={after_hash}")


if __name__ == "__main__":
    main()
