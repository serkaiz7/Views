import requests
import threading
import time
import random
import curses
from bs4 import BeautifulSoup

url = None
running = False
t = None
attempts = []

def run(stdscr):
    global running
    stdscr.clear()
    stdscr.nodelay(1)  # Make getch() non-blocking
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
            update_display(stdscr, f"Using proxy {proxy}. Response code: {response.status_code}")
            time.sleep(random.randint(15, 30))
        except Exception as e:
            end_time = time.time()
            attempts.append((end_time, proxy, f'Error: {e}'))
            update_display(stdscr, f"Error with proxy {proxy}: {e}")
            time.sleep(random.randint(15, 30))  # To prevent immediate retry with the same proxy
            pass

def start(stdscr):
    global t
    global running
    if not url:
        update_display(stdscr, "Error: Please set a video URL first.")
        return
    if running:
        update_display(stdscr, "Bot is already running.")
        return
    running = True
    t = threading.Thread(target=run, args=(stdscr,))
    t.start()
    update_display(stdscr, "Bot started.")

def stop(stdscr):
    global running
    if not running:
        update_display(stdscr, "Bot is not running.")
        return
    running = False
    t.join()
    update_display(stdscr, "Bot stopped.")

def get_proxy():
    r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all')
    proxies = r.content.decode().split('\r\n')
    proxies = [proxy for proxy in proxies if proxy]  # Remove empty entries
    return random.choice(proxies)

def menu(stdscr):
    global url
    while True:
        stdscr.clear()
        stdscr.addstr("Menu:\n")
        stdscr.addstr("1. Set URL\n")
        stdscr.addstr("2. Start Bot\n")
        stdscr.addstr("3. Stop Bot\n")
        stdscr.addstr("4. View Logs\n")
        stdscr.addstr("5. Exit\n")
        stdscr.addstr("Enter your choice: ")
        stdscr.refresh()
        choice = stdscr.getch()
        if choice == ord('1'):
            stdscr.addstr("Enter the video URL: ")
            stdscr.refresh()
            curses.echo()
            url = stdscr.getstr().decode()
            curses.noecho()
            update_display(stdscr, f"URL set to: {url}")
        elif choice == ord('2'):
            start(stdscr)
        elif choice == ord('3'):
            stop(stdscr)
        elif choice == ord('4'):
            view_logs(stdscr)
        elif choice == ord('5'):
            if running:
                stop(stdscr)
            break
        else:
            update_display(stdscr, "Invalid choice. Please enter a number between 1 and 5.")
        time.sleep(1)

def view_logs(stdscr):
    stdscr.clear()
    stdscr.addstr("Logs:\n")
    for attempt in attempts:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(attempt[0]))
        stdscr.addstr(f"Time: {timestamp}, Proxy: {attempt[1]}, Status: {attempt[2]}\n")
    stdscr.refresh()
    stdscr.getch()  # Wait for a key press to return to the menu

def update_display(stdscr, message):
    stdscr.clear()
    stdscr.addstr(message + "\n")
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
