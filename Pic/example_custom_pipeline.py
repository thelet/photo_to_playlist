"""
Example: Custom Pipeline Usage
Demonstrates how to use individual pipeline steps and modify configuration.
"""

from pipeline_steps import (
    step_initialize,
    step_generate_description,
    step_generate_params,
    step_generate_playlist,
    set_vision_provider,
    set_params_provider,
    get_configuration,
    get_run_record,
)
import json


def main():
    """
    Example of custom pipeline execution with configuration changes.
    """
    # ========================================================================
    # CONFIGURE THE PIPELINE
    # ========================================================================
    
    # Set vision model to use OpenAI
    set_vision_provider("openai", model="gpt-4o")
    
    # Set params generation to use Ollama
    set_params_provider("ollama", model="llama3.2")
    
    # Print configuration
    print("Pipeline Configuration:")
    print(json.dumps(get_configuration(), indent=2))
    print()
    
    # ========================================================================
    # EXECUTE PIPELINE STEPS
    # ========================================================================
    
    image_path = r'C:\Users\thele\OneDrive\Pictures\נעם\IMG_0730.JPG'
    
    # Step 1: Initialize
    run_id = step_initialize(image_path)
    print(f"Run ID: {run_id}\n")
    
    # Step 2: Generate description
    description = step_generate_description(run_id)
    print(f"Description keys: {list(description.keys())}\n")
    
    # You can modify configuration between steps if needed
    # For example, switch to OpenAI for params generation
    set_params_provider("openai", model="gpt-4o-mini")
    print("Switched to OpenAI for params generation\n")
    
    # Step 3: Generate parameters
    params = step_generate_params(run_id)
    print(f"Generated {len(params)} parameter fields\n")
    
    # Step 4: Generate playlist
    playlist_result = step_generate_playlist(run_id)
    playlist = playlist_result.get("playlist", [])
    print(f"Generated playlist with {len(playlist)} tracks\n")
    
    # ========================================================================
    # VIEW RESULTS
    # ========================================================================
    
    # Get full run record
    run_record = get_run_record(run_id)
    
    print("=" * 80)
    print("PIPELINE RESULTS SUMMARY")
    print("=" * 80)
    print(f"Run ID: {run_id}")
    print(f"Image: {run_record.get('image_path')}")
    print(f"Description: {run_record.get('description', {}).get('caption', 'N/A')}")
    print(f"Playlist Tracks: {len(run_record.get('Generated_Playlist', []))}")
    print("=" * 80)


if __name__ == "__main__":
    main()

