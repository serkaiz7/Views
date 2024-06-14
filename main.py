import requests
import threading
import time
import random

url = 'https://www.example.com'  # Replace with the URL you want to use
running = False

def run():
    global running
    running = True
    while running:
        try:
            proxy = get_proxy()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=5)
            time.sleep(random.randint(15, 30))
        except:
            pass

def start():
    global t
    global running
    t = threading.Thread(target=run)
    t.start()
    running = True

def stop():
    global running
    running = False
    t.join()

def get_proxy():
    r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all')
    proxies = r.content.decode().split('\r\n')
    return random.choice(proxies)

# Start the script
start()

# Let it run for a while then stop
time.sleep(60)  # Adjust this as needed
stop()
