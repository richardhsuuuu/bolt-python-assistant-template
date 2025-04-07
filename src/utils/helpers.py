import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def parse_slack_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and sanitize a Slack event payload
    """
    try:
        # Log the payload for debugging
        logger.debug(f"Received payload: {json.dumps(payload)}")
        
        # Return the cleaned payload
        return payload
    except Exception as e:
        logger.error(f"Error parsing Slack payload: {e}")
        return {}

def extract_user_info(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extract user information from a Slack payload
    """
    try:
        if "user" in payload:
            return payload["user"]
        elif "user_id" in payload:
            return {"id": payload["user_id"]}
        elif "event" in payload and "user" in payload["event"]:
            return {"id": payload["event"]["user"]}
        else:
            return None
    except Exception as e:
        logger.error(f"Error extracting user info: {e}")
        return None 
