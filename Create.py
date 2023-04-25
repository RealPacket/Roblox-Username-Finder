from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as Chrome
import time as task
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import betterLogging as Logger
import asyncio


class Birthday:
    """A birthday"""

    def __init__(self, Month: str, Day: int, Year: int):
        if Year > 2023:
            Logger.err("Invalid Birthday!")
            raise ValueError
        self.Month = Month
        self.Day = day
        self.Year = Year


async def set_random_birthday() -> bool:
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    month_dropdown: Chrome.WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "MonthDropdown")))
    day_dropdown: Chrome.WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DayDropdown")))
    year_dropdown: Chrome.WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "YearDropdown")))
    month_dropdown.click()
    month_dropdown.send_keys(random.choice(months))

    day_dropdown.click()
    day_dropdown.send_keys(random.randint(1, 29))

    year_dropdown.click()
    year_dropdown.send_keys(random.randint(1924, 2003))
    year_dropdown.click()
    return True


async def set_gender(Gender: str = "M"):
    Logger.info("setting random gender")
    MaleSelector: str = "MaleButton"
    FMSelector: str = "FemaleButton"
    Male: Chrome.WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, MaleSelector)))
    Female: Chrome.WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, FMSelector)))
    if Gender.startswith("M"):
        pass
        # Male.click()
    else:
        pass
        # Female.click()


def wait(secs: int):
    task.sleep(secs)


global task  # NOQA
task.wait = wait

options = Options()
driver = Chrome.Chrome(options=options, suppress_welcome=True)
driver.get("https://roblox.com/")


async def generate_username(length: int = 10):
    if type(length) != int:
        raise ValueError()
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=length))


async def generate_password(length: int = 100):
    return ''.join(random.choices(string.printable, k=length))


async def create_account(Username: str, Password: str) -> dict[str, str, bool]:
    """
    :param Username: The username of the new account.
    :param Password: The password of the new account.
    :return: A dictionary containing a username and password, and if it got successfully signed up.
    """
    try:
        Logger.info("Setting random birth day")
        await set_random_birthday()
        Logger.info("Starting to wait for password and username input")
        username_input: Chrome.webelement.WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signup-username"))
        )
        Logger.info("Username input found!")
        password_input: Chrome.webelement.WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signup-password"))
        )
        signup_button: Chrome.webelement.WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signup-button"))
        )
        validationError: Chrome.webelement.WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signup-userInputValidation"))
        )
        # #signup-usernameInputValidation is the thing that contains the error
        Logger.info("Password input found")
        username_input.send_keys(Username)
        Logger.info("username input filled out.")
        password_input.send_keys(Password)
        Logger.info("Attempting sign up...")
        try:
            if signup_button.get_property("Disabled") is not True and validationError.text == "":
                signup_button.click()
                Logger.info("Clicked signup button...")
        except:
            await create_account(Username, Password)
        print("\n" * 5)
        Logger.info(f"Username: {Username}\nPassword: {Password}")
        return {
            "Username": Username,
            "Password": Password,
            "Success": True
        }
    except Exception as e:
        Logger.err(str(e))


accountInfo = asyncio.run(create_account(asyncio.run(generate_username()), asyncio.run(generate_password())))
