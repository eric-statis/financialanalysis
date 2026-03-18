#!/usr/bin/env python3
"""
根据 adoption log 回滚正式 knowledge_base.json。
"""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Dict

from runtime_support import RuntimeConfigError, load_runtime_config, resolve_runtime_path


def now_iso() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


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
    parser = argparse.ArgumentParser(description="根据 adoption log 回滚正式 knowledge_base")
    parser.add_argument("--log", required=True, help="adoption log 路径")
    parser.add_argument("--runtime-config", help="显式指定 runtime/runtime_config.json")
    return parser.parse_args()



def main():
    args = parse_args()
    log_path = Path(args.log).resolve()
    if not log_path.exists():
        raise SystemExit(f"adoption log 不存在: {log_path}")

    try:
        runtime_config = load_runtime_config(
            config_path=Path(args.runtime_config) if args.runtime_config else None,
            cwd=Path.cwd(),
            require_knowledge_base=True,
            ensure_state_dirs=True,
        )
    except RuntimeConfigError as exc:
        raise SystemExit(str(exc)) from exc

    log_payload = read_json(log_path)
    knowledge_base_path = resolve_runtime_path(runtime_config, "knowledge_base")
    backup_path = Path(str(log_payload.get("backup_path", ""))).resolve()
    if not backup_path.exists():
        raise SystemExit(f"backup snapshot 不存在: {backup_path}")

    backup_payload = read_json(backup_path)
    restored_hash = md5_payload(backup_payload)
    write_json(knowledge_base_path, backup_payload)

    adoption_log_dir = resolve_runtime_path(runtime_config, "knowledge_adoption_log_dir")
    rollback_log_path = adoption_log_dir / f"{log_path.stem}.rollback.json"
    write_json(
        rollback_log_path,
        {
            "rolled_back_at": now_iso(),
            "source_log": str(log_path),
            "knowledge_base_path": str(knowledge_base_path),
            "backup_path": str(backup_path),
            "restored_hash": restored_hash,
        },
    )

    print(f"[OK] knowledge_base restored: {knowledge_base_path}")
    print(f"[OK] rollback_log: {rollback_log_path}")
    print(f"[OK] restored_hash={restored_hash}")


if __name__ == "__main__":
    main()
