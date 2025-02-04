from server import app as fastapi_app
from ui import app as gui_app, window
import uvicorn
import sys
import threading
import atexit
import os
import signal


def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


def stop_fastapi():
    print("Stopping FastAPI server...")
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    # Start the FastAPI server in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()

    # Register the stop_fastapi function to be called on exit
    atexit.register(stop_fastapi)

    # Start the PyQt GUI
    window.show()
    sys.exit(gui_app.exec())
