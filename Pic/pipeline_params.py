from __future__ import annotations

import json
import uuid
from typing import Any, Dict

try:
	from .params_store import get_param, save_param, create_run_file, read_run, set_run_field, run_path
	from .vision_handler import VisionHandler
	from .description_to_params import DescriptionToParams
	from .generate_deezer_playlist import DeezerPlaylistGenerator
except ImportError:
	from params_store import get_param, save_param, create_run_file, read_run, set_run_field, run_path  # type: ignore[no-redef]
	from vision_handler import VisionHandler  # type: ignore[no-redef]
	from description_to_params import DescriptionToParams  # type: ignore[no-redef]
	from generate_deezer_playlist import DeezerPlaylistGenerator  # type: ignore[no-redef]


def _run_key() -> str:
	"""
	Generate a unique id to use as the dedicated key in params_store.
	"""
	return uuid.uuid4().hex


def _get_run_record(run_id: str) -> Dict[str, Any]:
	"""
	Return the dict for a run id from its dedicated file.
	"""
	return read_run(run_id)


def run_pipeline(image_path: str) -> str:
	"""
	Pipeline:
	1) Save image_path under a new dedicated key id
	2) Retrieve image_path from store and run VisionHandler; save the description
	3) Retrieve description and run DescriptionToParams; save the params
	4) Generate playlist from song params and save it
	Returns the run id
	"""
	run_id = _run_key()

	# Step 1: save image path in a new dedicated file named <run_id>.json
	create_run_file(run_id, image_path)
	print(f"[step 1] image path saved. run_id={run_id}")
	print(f"          run file: {run_path(run_id)}")

	# Step 2: describe image using the stored path
	stored_path = _get_run_record(run_id).get("image_path")
	if not stored_path:
		raise RuntimeError("Image path missing in params_store")
	print("[step 2] starting to generate description...")
	vh = VisionHandler()
	description_json_str = vh.describe_image(stored_path)
	if not description_json_str:
		raise RuntimeError("Vision model returned empty description")
    
	print("[step 2] description generated.")
	print("[step 2] Generated description (raw JSON string):")
	print(description_json_str)
	description: Dict[str, Any] = json.loads(description_json_str)
	set_run_field(run_id, "description", description)
	print("[step 2] description saved.")

	# Step 3: convert description to Spotify params and save
	print("[step 3] starting to generate song params...")
	dtp = DescriptionToParams()
	desc_for_params = _get_run_record(run_id).get("description") or {}
	song_params: Dict[str, Any] = dtp.convert_to_params(desc_for_params)
	set_run_field(run_id, "song_params", song_params)
	print("[step 3] song params generated and saved.")

	# Step 4: generate playlist based on song params and save
	print("[step 4] starting to generate playlist from song params...")
	song_params_for_playlist: Dict[str, Any] = _get_run_record(run_id).get("song_params") or {}
	generator = DeezerPlaylistGenerator()
	result = generator.generate_playlist(song_params_for_playlist)
	playlist = result.get("playlist", [])
	set_run_field(run_id, "Generated_Playlist", playlist)
	set_run_field(run_id, "Generated_Playlist_Metadata", result.get("metadata", {}))
	print("[step 4] playlist generated and saved under 'Generated_Playlist'.")

	return run_id


def main() -> None:
	# Change this to your image path
	image_path = r'C:\Users\thele\OneDrive\Pictures\נעם\IMG_0730.JPG'
	run_id = run_pipeline(image_path)
	print(f"Pipeline completed. run_id={run_id}")


if __name__ == "__main__":
	main()


