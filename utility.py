from ruamel.yaml import YAML
from logger import logging
import tempfile
import os
import shutil


def update_env(dict_updated,env_file=".env"):
    """
    Update specified keys in a env file with new values.

    Args:
        Updates: A dict having new key values paires to update
    
    Raises:
        Exception: If an error occurs while updating the env file.
    """

    try:
      
        # Update environment variables for the current session
        for key, value in dict_updated.items():
            os.environ[key] = value

        # Read existing .env content if the file exists
        existing_vars = {}
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        existing_vars[k] = v

        # Merge new variables
        existing_vars.update(dict_updated)

        # Write updated variables back to the .env file
        with open(env_file, "w") as f:
            for key, value in existing_vars.items():
                f.write(f"{key}={value}\n")
    except Exception as e:
        logging.error(f"Error updating YAML file: {e}")
       
        raise e