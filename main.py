import requests
import threading
import time
import random
from bs4 import BeautifulSoup

url = None
running = False
t = None
attempts = []

def run():
    global running
    while running:
        try:
            proxy = get_proxy()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            start_time = time.time()
            response = requests.get(url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, headers=headers, timeout=5)
            status = 'Success' if response.status_code == 200 else 'Failed'
            end_time = time.time()
            attempts.append((end_time, proxy, status))
            print(f"Using proxy {proxy}. Response code: {response.status_code}")
            time.sleep(random.randint(15, 30))
        except Exception as e:
            end_time = time.time()
            attempts.append((end_time, proxy, f'Error: {e}'))
            print(f"Error with proxy {proxy}: {e}")
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
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = []
    for row in soup.find("table", {"id": "proxylisttable"}).find_all("tr")[1:]:
        columns = row.find_all("td")
        if columns[4].text.strip() == "elite proxy" and columns[6].text.strip() == "yes":
            proxy = f"{columns[0].text.strip()}:{columns[1].text.strip()}"
            proxy_list.append(proxy)
    return random.choice(proxy_list)

def menu():
    global url
    while True:
        print("\nMenu:")
        print("1. Set URL")
        print("2. Start Bot")
        print("3. Stop Bot")
        print("4. View Logs")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            url = input("Enter the video URL: ")
            print(f"URL set to: {url}")
        elif choice == '2':
            start()
        elif choice == '3':
            stop()
        elif choice == '4':
            view_logs()
        elif choice == '5':
            if running:
                stop()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def view_logs():
    print("\nLogs:")
    for attempt in attempts:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(attempt[0]))
        print(f"Time: {timestamp}, Proxy: {attempt[1]}, Status: {attempt[2]}")

if __name__ == "__main__":
    menu()
