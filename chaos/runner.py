# OWNER: P4
#
# PURPOSE:
# Orchestrate chaos experiments.
#
# RESPONSIBILITIES:
# Explain experiment orchestration.
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: None
# OUTPUT: None
#
# IMPLEMENTATION TODO:
# 1. Implement runner.

import os
import json
import yaml
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("chaos.runner")

# Import the experiments
from chaos.experiments import processor_kill, traffic_burst, bad_data, late_events

def load_config() -> Dict[str, Any]:
    """
    Load the config.yaml file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.yaml")
    
    if not os.path.exists(config_path):
        logger.warning(f"Config file not found at {config_path}. Using default settings.")
        return {}
        
    with open(config_path, "r") as f:
        try:
            return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Error reading YAML: {e}")
            return {}

def save_results(experiment_name: str, results: Dict[str, Any]):
    """
    Save the experiment results to the corresponding experiments/ directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Mapping experiment names to folders
    folder_mapping = {
        "processor_kill": "experiments/01_processor_restart/results.json",
        "traffic_burst": "experiments/02_traffic_burst/results.json",
        "bad_data": "experiments/03_bad_data/results.json",
        "late_events": "experiments/04_late_events/results.json"
    }
    
    relative_path = folder_mapping.get(experiment_name)
    if not relative_path:
        logger.error(f"Unknown experiment name: {experiment_name}")
        return
        
    output_path = os.path.join(project_root, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Saved results for {experiment_name} to {output_path}")

def run_all_experiments():
    """
    Orchestrate and run all four chaos experiments.
    """
    logger.info("Starting Chaos Orchestrator...")
    config = load_config()
    
    experiments = {
        "processor_kill": processor_kill.run_experiment,
        "traffic_burst": traffic_burst.run_experiment,
        "bad_data": bad_data.run_experiment,
        "late_events": late_events.run_experiment
    }
    
    summary = {}
    
    for name, run_func in experiments.items():
        logger.info("=" * 60)
        logger.info(f"Running Experiment: {name}")
        logger.info("=" * 60)
        
        try:
            results = run_func(config)
            save_results(name, results)
            summary[name] = "SUCCESS"
        except Exception as e:
            logger.error(f"Experiment {name} failed: {e}", exc_info=True)
            summary[name] = f"FAILED: {e}"
            
    logger.info("=" * 60)
    logger.info("Chaos Experiment Orchestration Summary:")
    for name, status in summary.items():
        logger.info(f" - {name}: {status}")
    logger.info("=" * 60)

if __name__ == "__main__":
    run_all_experiments()
