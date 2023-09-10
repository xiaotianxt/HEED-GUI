import requests
import base64
from PIL import Image
from io import BytesIO

from config import get_captcha_password, get_captcha_username


def recognize(img: Image.Image) -> str:
    """
    Recognize captcha using external API.

    :param img: PIL.Image object
    :return: recognized text as string
    """

    # Convert PIL.Image to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # API Endpoint
    url = "http://api.ttshitu.com/predict"

    # API request payload
    payload = {
        "username": get_captcha_username(),
        "password": get_captcha_password(),
        "typeid": "1003",
        "image": img_str,
    }

    headers = {"Content-Type": "application/json"}

    # Sending POST request to API
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            return data["data"]["result"]
        else:
            print(f"API Error: {data['message']}")
            return "ERROR"
    else:
        print(f"HTTP Error: {response.status_code}")
        return "ERROR"


if __name__ == "__main__":
    # Test
    img = Image.open("captcha.png")
    print(recognize(img))
