"""
Pipeline Orchestrator
Main script that orchestrates the pipeline steps in the correct order.
"""

from __future__ import annotations

from typing import Optional

try:
    from .pipeline_steps import (
        step_initialize,
        step_generate_description,
        step_generate_params,
        step_generate_playlist,
        set_vision_provider,
        set_params_provider,
        set_playlist_generator,
        get_configuration,
        get_run_record,
    )
except ImportError:
    from pipeline_steps import (
        step_initialize,
        step_generate_description,
        step_generate_params,
        step_generate_playlist,
        set_vision_provider,
        set_params_provider,
        set_playlist_generator,
        get_configuration,
        get_run_record,
    )


def run_pipeline(image_path: str) -> str:
    """
    Run the complete photo-to-playlist pipeline.
    Executes all steps in order: initialization, description, params, playlist.
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        str: The run_id for this pipeline execution
    """
    set_params_provider("openai", model="gpt-4o-mini")
    set_vision_provider("openai", model="gpt-4o-mini")
    # Step 1: Initialize
    run_id = step_initialize(image_path)
    
    # Step 2: Generate description
    step_generate_description(run_id)
    
    # Step 3: Generate parameters
    step_generate_params(run_id)
    
    # Step 4: Generate playlist
    step_generate_playlist(run_id)
    
    return run_id


def main() -> None:
    """
    Main function - configure and run the pipeline.
    Modify configuration here or use the setter functions.
    """
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    # You can modify the configuration here or use the setter functions:
    
    # Example: Use OpenAI for vision
    # set_vision_provider("openai", model="gpt-4o")
    
    # Example: Use Ollama for params (default)
    # set_params_provider("ollama", model="llama3.2")
    
    # Example: Use OpenAI for params
    # set_params_provider("openai", model="gpt-4o-mini")
    
    # Print current configuration
    print("Current Pipeline Configuration:")
    config = get_configuration()
    import json
    print(json.dumps(config, indent=2))
    print()
    
    # ========================================================================
    # RUN PIPELINE
    # ========================================================================
    # Change this to your image path
    image_path = r'D:\thelet\photo_to_playlist\test_img\beach.jpg'
    
    run_id = run_pipeline(image_path)
    print(f"\n✅ Pipeline completed successfully!")
    print(f"   run_id: {run_id}")
    
    # Optionally, print the final result
    # run_record = get_run_record(run_id)
    # print(f"\nFinal run record:")
    # print(json.dumps(run_record, indent=2, default=str))


if __name__ == "__main__":
    main()
