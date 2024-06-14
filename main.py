import requests
import threading
import time
import random
import os
import sys

url = 'https://www.example.com'  # Replace with the URL you want to use
running = False
proxies = []
current_proxy = ''
next_proxy = ''

def matrix_print(text, delay=0.05):
    for char in text + '\n':
        sys.stdout.write(f'\033[32m{char}\033[0m')
        sys.stdout.flush()
        time.sleep(delay)

def get_proxies():
    global proxies
    r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all')
    proxies = r.content.decode().split('\r\n')

def get_proxy():
    global current_proxy, next_proxy
    if not proxies:
        get_proxies()
    current_proxy = random.choice(proxies)
    next_proxy = random.choice(proxies)
    return current_proxy

def run():
    global running
    while running:
        try:
            proxy = get_proxy()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=5)
            os.system('clear')
            matrix_print(f"Current Proxy: {current_proxy}")
            matrix_print(f"Next Proxy: {next_proxy}")
            if response.status_code == 200:
                matrix_print("Success!")
            else:
                matrix_print("Failed!")
            time.sleep(random.randint(15, 30))
        except Exception as e:
            matrix_print(f"Error: {e}")
            time.sleep(5)

def start():
    global t
    global running
    running = True
    t = threading.Thread(target=run)
    t.start()

def stop():
    global running
    running = False
    t.join()

def main_menu():
    while True:
        os.system('clear')
        print("Menu:")
        print("1. Add YouTube URL")
        print("2. Start")
        print("3. Stop")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            global url
            url = input("Enter YouTube URL: ")
        elif choice == '2':
            if not running:
                start()
                print("Started!")
            else:
                print("Already running!")
        elif choice == '3':
            if running:
                stop()
                print("Stopped!")
            else:
                print("Not running!")
        elif choice == '4':
            if running:
                stop()
            break
        else:
            print("Invalid choice!")
        time.sleep(1)

if __name__ == "__main__":
    main_menu()
