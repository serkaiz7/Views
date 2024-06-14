import requests
import threading
import time
import random
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url = None
running = False
t = None
attempts = []
proxies_used = []

# Flask server
app = Flask(__name__)

@app.route('/data')
def get_data():
    return jsonify({'attempts': attempts, 'proxies_used': proxies_used})

# Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

dash_app.layout = html.Div(children=[
    html.H1(children='YouTube View Bot Dashboard'),
    dcc.Graph(id='attempt-graph'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
])

@dash_app.callback(Output('attempt-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.DataFrame(attempts, columns=['Time', 'Proxy', 'Status'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df.index, mode='lines+markers', name='Attempts'))
    fig.update_layout(title='Proxy Attempts', xaxis_title='Time', yaxis_title='Attempts')
    return fig

def run():
    global running
    while running:
        try:
            proxy = get_proxy()
            proxies_used.append(proxy)
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
    threading.Thread(target=menu).start()
    app.run(debug=True, use_reloader=False)
