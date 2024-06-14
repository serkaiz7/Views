import requests
import threading
import time
import random

url = None
running = False
t = None

def run():
    global running
    while running:
        try:
            proxy = get_proxy()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=5)
            time.sleep(random.randint(15, 30))
        except:
            pass

def start():
    global t
    global running
    if not url:
        print("Error: Please set a video URL first.")
        return
    if running:
        print("Bot is already running.")
        return
    running = True
    t = threading.Thread(target=run)
    t.start()
    print("Bot started.")

def stop():
    global running
    if not running:
        print("Bot is not running.")
        return
    running = False
    t.join()
    print("Bot stopped.")

def get_proxy():
    r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all')
    proxies = r.content.decode().split('\r\n')
    return random.choice(proxies)

def menu():
    global url
    while True:
        print("\nMenu:")
        print("1. Set URL")
        print("2. Start Bot")
        print("3. Stop Bot")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            url = input("Enter the video URL: ")
            print(f"URL set to: {url}")
        elif choice == '2':
            start()
        elif choice == '3':
            stop()
        elif choice == '4':
            if running:
                stop()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    menu()
