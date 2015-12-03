import time
import threading
import webbrowser
from batman_splash import start_app

def start_browser(server_ready_event, url):
	server_ready_event.wait()
	webbrowser.open(url)

if __name__ == '__main__':
	url = 'http://localhost:5000'
	server_ready = threading.Event()
	browser_thread = threading.Thread(target=start_browser,
					  args = (server_ready, url))
	browser_thread.start()
	server_ready.set()
	start_app()
	browser_thread.join()
