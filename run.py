import os
from threading import Timer
import threading
import webbrowser
from app import app

def open_browser():
    webbrowser.open_new_tab('http://localhost:5000')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    Timer(1, open_browser).start()
    app.run(debug=True, port=port, use_reloader=False)


    thread = threading.Timer(1.5, open_browser)
    thread.start()

