import json
from src.utils.logger import logger

def save_state(state, file_path="conversation_state.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(state, f, indent=2)
        logger.info(f"Conversation state saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save conversation state: {e}")

def load_state(file_path="conversation_state.json"):
    try:
        with open(file_path, "r") as f:
            state = json.load(f)
        logger.info(f"Conversation state loaded from {file_path}")
        return state
    except FileNotFoundError:
        logger.info(f"No state file found at {file_path}, returning empty state")
        return {}
    except Exception as e:
        logger.error(f"Failed to load conversation state: {e}")
        return {}