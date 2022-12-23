import subprocess
import sys
import time as T
import string
import random
import time
from json import loads as Decode

# Set the URL and the parameters
url = "https://auth.roblox.com/v1/usernames/validate"

try:
    import requests as R
except ImportError:
    option = input("Should we install the requests library for you? (Y/N)").lower()
    if option == "y" or option == "yes":
        subprocess.run(["pip", "install", "requests"])
        T.sleep(4)
        import requests as R
    else:
        print("You entered No, please install the requests library to continue. To install the requests library, "
              "run `pip install requests`.")
        sys.exit(1)
try:
    import keyboard as K
except ImportError:
    option = input("Should we install the keyboard library for you? (Y/N)").lower()
    if option == "y" or option == "yes":
        subprocess.run(["pip", "install", "keyboard"])
        import keyboard as K
    else:
        print(
            f"You entered {option}, please install the keyboard library to continue. To install the keyboard library, "
            "run `pip install keyboard`.")
        sys.exit(1)


# Set the URL and the parameters
url = "https://auth.roblox.com/v1/usernames/validate"
params = {"context": "Signup", "Birthday": "1931-01-01T06:00:00.000Z"}

# Set the delay between requests (in seconds)
delay = 6

while not K.is_pressed("Q"):
    # Generate a random 5-letter string
    username = "".join(random.choices(string.ascii_letters, k=5))

    # Update the parameters with the random username
    params["username"] = username

    # Make the request
    response: R.Response = R.get(url, params=params)

    # Decode the response text
    data = Decode(response.text)

    # Print the message object
    print(f"[{username}] {data['message']}")
    # {'code': 1, 'message': 'Username is already in use'}

    # Delay the next request
    time.sleep(delay)
