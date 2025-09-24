"""Send a notification to the user. through SMS or Email
"""

import vonage
import os
import httpx

from dotenv import load_dotenv

from .api_logger import logger

load_dotenv()


def send_sms_notification(to: str, message: str) -> bool:
    """Send an SMS to the user.

    Args:
        to (str): The phone number to send the SMS to.
        message (str): The message to send.

    Returns:
        **bool**: True if the SMS was sent successfully, False otherwise.
    """
    url = "https://rest.nexmo.com/sms/json"

    payload = {
        "from": "Vonage APIs",
        "text": message,
        "to": to,
        "api_key": f"{os.getenv('VONAGE_API_KEY')}",
        "api_secret": f"{os.getenv('VONAGE_API_SECRET')}",
    }

    # Synchronous request
    response = httpx.post(url, data=payload)

    if response.status_code == 200:
        logger.info(f"SMS sent successfully to {to}")
        return True
    else:
        logger.error(f"Failed to send SMS to {to}: {response.text}")
        return False
