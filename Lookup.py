import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import sys
import os
import platform
from colorama import Fore, Style

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def get_roblox_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    data = {"usernames": [username], "excludeBannedUsers": True}
    response = requests.post(url, json=data)
    if response.status_code == 200 and response.json().get("data"):
        return response.json()["data"][0]["id"]
    return None

def get_rolimons_value(user_id):
    url = f"https://www.rolimons.com/player/{user_id}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        
        value_element = driver.find_element(By.ID, "player_value")
        rap_element = driver.find_element(By.ID, "player_rap")
        
        value = value_element.text.strip() if value_element else "No value found"
        rap = rap_element.text.strip() if rap_element else "No RAP found"
        
        return value, rap
    except Exception:
        return "Invalid user ID", "No data available"
    finally:
        driver.quit()

def main():
    logging.getLogger("selenium").setLevel(logging.CRITICAL)
    sys.stderr = open(os.devnull, "w")
    
    while True:
        username = input("Enter Roblox username (or type 'exit' to quit): ")
        if username.lower() == 'exit':
            break
        
        user_id = get_roblox_user_id(username)
        if not user_id:
            clear_console()
            print("Invalid username or user not found.")
            continue
        
        value, rap = get_rolimons_value(user_id)
        roblox_profile = f"https://www.roblox.com/users/{user_id}/profile"
        rolimons_profile = f"https://www.rolimons.com/player/{user_id}"
        
        clear_console()
        print(f"{username}'s Rolimon's Info:")
        print(Fore.GREEN + f"Value: {value}, RAP: {rap}" + Style.RESET_ALL)
        print(f"\nRoblox Profile: {Fore.BLUE}{roblox_profile}{Style.RESET_ALL}")
        print(f"Rolimon's Profile: {Fore.BLUE}{rolimons_profile}{Style.RESET_ALL}")
        
        print(f"\nVisit my GitHub profile and give a {Fore.YELLOW}star{Style.RESET_ALL} for my projects if you appreciate my hard work! {Fore.BLUE}https://github.com/dx9g{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
