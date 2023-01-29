import concurrent.futures
import json
import random
import string
from typing import Dict

import requests


# Set the URL and the parameters
url = "https://auth.roblox.com/v1/usernames/validate"
# fake birthday
params = {"context": "Signup", "Birthday": "1931-01-01T06:00:00.000Z"}

# Set the delay between requests (in seconds)
# delay = 1 or float(sys.argv[0])
RetryTimes: int = 0


def generate_random_username(length: int = 5) -> str:
    """
    This function generates a random string of the specified length.
    """
    return "".join(random.choices(string.ascii_letters, k=length))


def check_username_availability(username: str) -> Dict[str, str]:
    """
    This function checks the availability of a given name on the specified URL.
    """
    # Update the parameters with the random name
    params["username"] = username
    # Make the request
    response = requests.get(url, params=params)
    # Decode the response text
    rData = json.loads(response.text)
    return rData


# Use a ThreadPoolExecutor to run the check_username_availability function concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    future_to_name = {
        executor.submit(check_username_availability,
                        generate_random_username()): generate_random_username() for i in range(1000)}
    for future in concurrent.futures.as_completed(future_to_name):
        name = future_to_name[future]
        try:
            data = future.result()
            if not data['message'] or not data['code']:
                print(f"[{name}] No message or code. can't tell if claimed or not.")
            if data["code"] != 0:
                print(f"[{name}] {data['message']}")
            else:
                print(f"{name} isn't claimed!")
        except (requests.RequestException, requests.ConnectionError,
                ConnectionResetError, ConnectionError,
                ConnectionRefusedError, ConnectionAbortedError):
            print(f"[{RetryTimes}] Retrying...")
            continue
