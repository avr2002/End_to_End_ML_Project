import os
from datetime import datetime


ROOT_DIR = os.getcwd()

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


# Training Pipeline related Variables
# The values that are used here are same as in config.yaml file, Here we have defined contants(names) to directly access 
# their values, like if we need 'pipeline_name: housing' from config.yaml file, we can access it's value(housing) from variable
# TRAINING_PIPELINE_NAME_KEY
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
