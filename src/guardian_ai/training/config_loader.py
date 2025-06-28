import json
from pathlib import Path
from transformers import TrainingArguments

# Define the path to the default config
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "configs/training/default_trainer_args.json"

def load_and_validate_training_args(stage_specific_config_path: str) -> TrainingArguments:
    """
    Loads training configurations, merges defaults, validates, and returns
    a TrainingArguments object.

    This function provides a single, robust entry point for all training jobs.
    """
    # 1. Smooth Loading with Error Handling
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as f:
            # Start with the safe, default settings
            final_config = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"FATAL: Default config not found at {DEFAULT_CONFIG_PATH}")
    except json.JSONDecodeError:
        raise RuntimeError(f"FATAL: Default config at {DEFAULT_CONFIG_PATH} is not valid JSON.")

    try:
        with open(stage_specific_config_path, 'r') as f:
            stage_config = json.load(f)
            # Merge: The stage-specific config overrides the defaults
            final_config.update(stage_config)
    except FileNotFoundError:
        raise RuntimeError(f"FATAL: Stage-specific config not found at {stage_specific_config_path}")
    except json.JSONDecodeError:
        raise RuntimeError(f"FATAL: Stage-specific config at {stage_specific_config_path} is not valid JSON.")
    
    # 2. Validation for Required Arguments
    # Ensure critical, non-default arguments are present
    required_keys = ["output_dir"]
    for key in required_keys:
        if key not in final_config:
            raise ValueError(f"Missing required argument '{key}' in the final merged configuration.")

    # 3. Clean the config by removing our custom _comment keys before passing to Transformers
    final_config_cleaned = {k: v for k, v in final_config.items() if not k.startswith('_')}

    print("✅ Configuration loaded and validated successfully.")
    
    # 4. Return a structured object, not a loose dictionary
    return TrainingArguments(**final_config_cleaned)

# Example of a 'smoother' main training function
def main_training_flow(config_path: str):
    """
    The main training function is now incredibly clean.
    It only needs to know about one thing: the path to the config file.
    """
    print(f"--- Starting training run with config: {config_path} ---")
    training_args = load_and_validate_training_args(config_path)
    
    # ... rest of the training logic (loading model, dataset, trainer, etc.)
    # trainer.train()
    
    print("--- Training run finished. ---")