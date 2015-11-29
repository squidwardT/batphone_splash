import time
import threading
import webbrowser
from batman_splash import start_app

thread = threading.Thread(target=webbrowser.open, args=('http://localhost:5000',))
thread.start()
start_app()
