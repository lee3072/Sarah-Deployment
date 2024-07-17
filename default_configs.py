"""
default_configs.py

Author: Seung Heon Lee (University of Southern California, HaRVI Lab)

This file contains default configurations and utility functions for managing
application settings, case configurations, and experiment configurations. It
provides functions for loading, saving, and initializing configuration files.
"""

import os
import json

# Default folder paths for the GUI application
DEFAULT_GUI_FOLDER = '.gui'
DEFAULT_SETTINGS_FOLDER = '.gui/setting'
DEFAULT_CASE_FOLDER = '.gui/case'
DEFAULT_EXPERIMENT_FOLDER = '.gui/experiment'

# Default file paths for the GUI application
DEFAULT_SETTINGS_PATH = os.path.join(DEFAULT_SETTINGS_FOLDER, 'default.json')
LAST_ACCESSED_SETTINGS_PATH = os.path.join(DEFAULT_SETTINGS_FOLDER, 'last_saved')
DEFAULT_CASE_PATH = os.path.join(DEFAULT_CASE_FOLDER, 'default.json')
LAST_ACCESSED_CASE_PATH = os.path.join(DEFAULT_CASE_FOLDER, 'last_saved')
DEFAULT_EXPERIMENT_PATH = os.path.join(DEFAULT_EXPERIMENT_FOLDER, 'default.json')
LAST_ACCESSED_EXPERIMENT_PATH = os.path.join(DEFAULT_EXPERIMENT_FOLDER, 'last_saved')

# Default settings for the GUI application
default_settings = {
    "github_id": "lee3072",
    "github_repo": "TouchTactServer",
    "ServerAddress": "https://lee3072.github.io/TouchTactServer",
    "use_server_address": False,
    "FolderVariables": {
        "OriginalAudioFolder": os.path.join("Files", "Audio", "Original"),
        "LatencyAudioFolder": os.path.join("Files", "Audio", "Latency"),
        "OriginalHapticFolder": os.path.join("Files", "Haptic", "Original"),
        "LatencyHapticFolder": os.path.join("Files", "Haptic", "Latency"),
        "ImageFolder": os.path.join("Files", "Image"),
        "CaseFolder": os.path.join("Files", "Case"),
        "ExperimentFolder": os.path.join("Files", "Experiment")
    },
    "user_agreements": [
        "I will read instruction out loud",
        "I will participate in the study",
        "I will provide honest responses",
        "I consent to collect interaction data",
        "My participation is voluntary",
        "I can withdraw from the study any time"
    ],
    "Links": [
        {"nickname": "example_survey", "url": "https://usc.qualtrics.com/jfe/form/SV_41rUA1Ng0oC6Pe6"}
    ],
    "layout_descriptions": [
        {"image": "Files/Image/Layout0_tap.png", "location_array_available": False, "interaction_type": "tap"},
        {"image": "Files/Image/Layout1_tap.png", "location_array_available": True, "interaction_type": "tap"},
        {"image": "Files/Image/Layout1_swipe.png", "location_array_available": True, "interaction_type": "swipe_through"}
    ]
}

# Default configuration for a case in the GUI application
default_case_config = {
    "case_id": "",
    "interaction": "tap & continue",
    "order_array": [str(i + 1) for i in range(9)],
    "custom_text_array": [str(i + 1) for i in range(9)],
    "interaction_delay": ["0"] * 9,
    "location_array": [{"x": "50", "y": "50"} for _ in range(9)],
    "highlight_array": [str(i + 1) for i in range(9)],
    "timer": {
        "enabled": False,
        "direction": "up",
        "max_time": "7000",
        "format": "S",
        "fake_ranking": "5632",
        "fake_ranking_enabled": False
    },
    "scoreboard": {
        "enabled": False,
        "reward_score": "100",
        "penalty_percentage": "2",
        "decimal_places": "0",
        "display_negative": False,
        "fake_ranking": "100",
        "fake_ranking_enabled": False
    },
    "linked_files": {
        "correct_haptic": ["None"]*9,
        "wrong_haptic": ["None"]*9,
        "correct_audio": ["None"]*9,
        "wrong_audio": ["None"]*9,
    },
    "tutorial_text": {
        "interaction_type": "tap on the button from 1 to 9",
        "penalty": "incorrect interaction will result in a penalty",
        "game_mode": "you will be able to continue from the button you left off if you make a mistake",
    },
    "game_over_text": "Congratulations! You have completed the game!",
    "survey_url": "",
    "custom_text_enabled": False,
    "location_array_enabled": False,
    "highlight_array_enabled": False,
}

# Default configuration for an experiment in the GUI application
default_experiment_config = {
    "ExperimentID": "",
    "CaseFiles": [],
    "survey_url": ""
}

def initialize_config_files():
    """
    Ensures that the default settings and case files exist.
    If they don't exist, creates them with the default values.
    """
    # Ensure the default settings file exists
    if not os.path.exists(DEFAULT_SETTINGS_PATH):
        os.makedirs(os.path.dirname(DEFAULT_SETTINGS_PATH), exist_ok=True)
        with open(DEFAULT_SETTINGS_PATH, 'w') as f:
            json.dump(default_settings, f, indent=4)
    
    # Ensure the last saved settings file exists
    if not os.path.exists(LAST_ACCESSED_SETTINGS_PATH):
        os.makedirs(os.path.dirname(LAST_ACCESSED_SETTINGS_PATH), exist_ok=True)
        update_last_used_file_record(LAST_ACCESSED_SETTINGS_PATH, DEFAULT_SETTINGS_PATH)

    # Ensure the default case file exists
    if not os.path.exists(DEFAULT_CASE_PATH):
        os.makedirs(os.path.dirname(DEFAULT_CASE_PATH), exist_ok=True)
        with open(DEFAULT_CASE_PATH, 'w') as f:
            json.dump(default_case_config, f, indent=4)

    # Ensure the last saved case file exists
    if not os.path.exists(LAST_ACCESSED_CASE_PATH):
        os.makedirs(os.path.dirname(LAST_ACCESSED_CASE_PATH), exist_ok=True)
        update_last_used_file_record(LAST_ACCESSED_CASE_PATH, DEFAULT_CASE_PATH)

    # Ensure the default experiment file exists
    if not os.path.exists(DEFAULT_EXPERIMENT_PATH):
        os.makedirs(os.path.dirname(DEFAULT_EXPERIMENT_PATH), exist_ok=True)
        with open(DEFAULT_EXPERIMENT_PATH, 'w') as f:
            json.dump(default_experiment_config, f, indent=4)

    # Ensure the last saved experiment file exists
    if not os.path.exists(LAST_ACCESSED_EXPERIMENT_PATH):
        os.makedirs(os.path.dirname(LAST_ACCESSED_EXPERIMENT_PATH), exist_ok=True)
        update_last_used_file_record(LAST_ACCESSED_EXPERIMENT_PATH, DEFAULT_EXPERIMENT_PATH)

def update_last_used_file_record(acess_record_path, file_path):
    """
    Updates the last accessed settings file with the specified file path.
    
    Args:
        file_path (str): The file path to update the last accessed settings file with.
    """
    with open(acess_record_path, 'w') as f:
        json.dump({"last_accessed_file": file_path}, f, indent=4)

def load_setting(file_path = None):
    """
    Ensures that the default settings and case files exist before loading the settings.
    Loads the settings from the specified file path.
    If the file path is None, loads the settings from the last saved settings file.
    
    Returns:
        dict: The loaded settings.
    """
    # Ensure the default settings and case files exist
    initialize_config_files()
    # If the file path is not specified, load the target setting path from the last saved settings file
    if file_path is None:
        with open(LAST_ACCESSED_SETTINGS_PATH, 'r') as f:
            file_path = json.load(f)["last_accessed_file"]
    # Update the last accessed settings file with the specified file path
    update_last_used_file_record(LAST_ACCESSED_SETTINGS_PATH, file_path)
    # Load the settings from the specified file path
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Load Setting: {file_path} is not a valid JSON file.")
        except FileNotFoundError:
            raise FileNotFoundError("Load Setting: {file_path} file does not exist.")

def load_case_config(file_path = None):
    """
    Ensures that the default settings and case files exist before loading the settings.
    Loads the case configuration from the specified file.
    If the file path is None, loads the case configuration from the default case file.

    Args:
        file_path (str): The path to the case configuration file.
    
    Returns:
        dict: The loaded case configuration.
    """
    # Ensure the default settings and case files exist
    initialize_config_files()
    # Load the case configuration from the specified file path
    if file_path is None:
        with open(LAST_ACCESSED_CASE_PATH, 'r') as f:
            file_path = json.load(f)["last_accessed_file"]
    # Update the last accessed case file with the specified file path
    update_last_used_file_record(LAST_ACCESSED_CASE_PATH, file_path)
    # Load the case configuration from the specified file path
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Load Case Config: {file_path} is not a valid JSON file.")
        except FileNotFoundError:
            raise FileNotFoundError("Load Case Config: {file_path} file does not exist.")

def load_experiment_config(file_path = None):
    """
    Ensures that the default settings and case files exist before loading the settings.
    Loads the experiment configuration from the specified file.
    If the file path is None, loads the experiment configuration from the default experiment file.

    Args:
        file_path (str): The path to the experiment configuration file.
    
    Returns:
        dict: The loaded experiment configuration.
    """
    # Ensure the default settings and case files exist
    initialize_config_files()
    # Load the experiment configuration from the specified file path
    if file_path is None:
        with open(LAST_ACCESSED_EXPERIMENT_PATH, 'r') as f:
            file_path = json.load(f)["last_accessed_file"]
    # Update the accessed experiment file with the specified file path
    update_last_used_file_record(LAST_ACCESSED_EXPERIMENT_PATH, file_path)
    # Load the experiment configuration from the specified file path
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Load Experiment Config: {file_path} is not a valid JSON file.")
        except FileNotFoundError:
            raise FileNotFoundError("Load Experiment Config: {file_path} file does not exist.")