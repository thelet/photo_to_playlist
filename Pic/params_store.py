from __future__ import annotations

"""
Lightweight parameter store for other modules.
- Stores a single JSON file under <project_root>/params (or PARAMS_DIR).
- Provides functions: get_param, save_param, get_all, save_params.
- Includes a tiny CLI: `python Pic/params_store.py get <key>` or `save <key> <json_value>`.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

PARAMS_DIR_ENV = "PARAMS_DIR"
PARAMS_FILENAME = "params.json"
LOCAL_DB_DIR_ENV = "LOCAL_DB_DIR"  # for per-run files (database folder)


def _resolve_dir() -> Path:
	"""
	Resolve the params directory.
	Priority: env PARAMS_DIR -> <project_root>/params
	"""
	env_dir = os.getenv(PARAMS_DIR_ENV)
	if env_dir:
		dir_path = Path(env_dir)
	else:
		# Pic/params_store.py -> project root is parent of Pic
		dir_path = Path(__file__).resolve().parent.parent / "params"
	dir_path.mkdir(parents=True, exist_ok=True)
	return dir_path


def _params_path() -> Path:
	return _resolve_dir() / PARAMS_FILENAME


def _load() -> Dict[str, Any]:
	p = _params_path()
	if not p.exists():
		return {}
	with open(p, "r", encoding="utf-8") as f:
		return json.load(f)


def _save(data: Dict[str, Any]) -> None:
	p = _params_path()
	with open(p, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def get_param(key: str, default: Optional[Any] = None) -> Any:
	"""
	Return the value for a key; default if missing.
	"""
	return _load().get(key, default)


def save_param(key: str, value: Any) -> None:
	"""
	Save/overwrite a single key/value pair.
	"""
	data = _load()
	data[key] = value
	_save(data)


def get_all() -> Dict[str, Any]:
	"""
	Return the full parameter dictionary.
	"""
	return _load()


def save_params(items: Dict[str, Any]) -> None:
	"""
	Merge-save multiple keys at once.
	"""
	data = _load()
	data.update(items)
	_save(data)


def _parse_json_value(raw: str) -> Any:
	"""
	Parse a raw string as JSON if possible; fallback to raw string.
	"""
	try:
		return json.loads(raw)
	except Exception:
		return raw


# ------------------------------
# Per-run files in "database" dir
# ------------------------------

def _runs_dir() -> Path:
	"""
	Resolve the 'database' directory to keep one JSON file per run.
	Priority: env LOCAL_DB_DIR -> <project_root>/database
	"""
	env_path = os.getenv(LOCAL_DB_DIR_ENV)
	if env_path:
		db_dir = Path(env_path)
	else:
		db_dir = Path(__file__).resolve().parent.parent / "database"
	db_dir.mkdir(parents=True, exist_ok=True)
	return db_dir


def run_path(run_key: str) -> Path:
	"""
	Full path for the run file. The filename is the key identifier.
	"""
	return _runs_dir() / f"{run_key}.json"


def create_run_file(run_key: str, image_path: str) -> None:
	"""
	Create a new run file named <run_key>.json with the initial payload.
	Overwrites if already exists.
	"""
	payload: Dict[str, Any] = {
		"key": run_key,
		"image_path": image_path,
		"description": None,
		"song_params": None,
		"Generated_Playlist": None,
	}
	with open(run_path(run_key), "w", encoding="utf-8") as f:
		json.dump(payload, f, indent=2, ensure_ascii=False)


def read_run(run_key: str) -> Dict[str, Any]:
	"""
	Load the run JSON as a dict.
	"""
	p = run_path(run_key)
	if not p.exists():
		raise FileNotFoundError(f"Run file not found: {p}")
	with open(p, "r", encoding="utf-8") as f:
		return json.load(f)


def write_run(run_key: str, payload: Dict[str, Any]) -> None:
	"""
	Overwrite the run JSON with the provided payload.
	"""
	with open(run_path(run_key), "w", encoding="utf-8") as f:
		json.dump(payload, f, indent=2, ensure_ascii=False)


def set_run_field(run_key: str, field: str, value: Any) -> None:
	"""
	Set a single field in the run JSON and save.
	"""
	data = read_run(run_key)
	data[field] = value
	write_run(run_key, data)


def _cli() -> None:
	"""
	Very small CLI:
	  get <key>
	  save <key> <json_or_string_value>
	  get_all
	  save_many <json_object>
	"""
	import sys
	if len(sys.argv) < 2:
		print("Usage: python Pic/params_store.py [get|save|get_all|save_many] ...")
		sys.exit(1)
	cmd = sys.argv[1].lower()
	if cmd == "get":
		if len(sys.argv) < 3:
			print("Usage: get <key>")
			sys.exit(1)
		key = sys.argv[2]
		val = get_param(key)
		print(json.dumps(val, ensure_ascii=False))
	elif cmd == "save":
		if len(sys.argv) < 4:
			print("Usage: save <key> <json_or_string_value>")
			sys.exit(1)
		key = sys.argv[2]
		value = _parse_json_value(sys.argv[3])
		save_param(key, value)
		print(f"saved: {key}")
	elif cmd == "get_all":
		print(json.dumps(get_all(), indent=2, ensure_ascii=False))
	elif cmd == "save_many":
		if len(sys.argv) < 3:
			print("Usage: save_many <json_object>")
			sys.exit(1)
		payload = _parse_json_value(sys.argv[2])
		if not isinstance(payload, dict):
			print("save_many expects a JSON object")
			sys.exit(1)
		save_params(payload)
		print("saved many")
	else:
		print(f"Unknown command: {cmd}")
		sys.exit(1)


if __name__ == "__main__":
	_cli()


