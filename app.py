import os
import sys
import datetime
import urllib.request
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from flask import Flask, send_file, request


# Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler(
    'spy_pixel_logs.log',
    maxBytes=5000000,
    backupCount=5
)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(handler)

# Flask
app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

@app.route('/')
def home():
    spy_meme = os.path.join(STATIC_ROOT, 'spy_meme.gif')
    return send_file(spy_meme, mimetype="image/gif")

@app.route('/image')
def spy_pixel():
    filename = os.path.join(STATIC_ROOT, 'pixel.png')

    # Log the User-Agent String.
    user_agent = request.headers.get('User-Agent')

    # Get the current time of request and format time into readable format.
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

    # Log the IP address of requester.
    get_ip = request.remote_addr

    # Lookup Geolocation of IP Address.
    with urllib.request.urlopen("https://geolocation-db.com/jsonp/"+ get_ip) as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")

    # Add User-Agent, Timestamp, and IP Address + Geolocation information to dictionary.
    log_entry = f"Timestamp: {timestamp}\nUser Agent: {user_agent}\nIP Address: {data}"
    logger.info(log_entry)

    return send_file(filename, mimetype="image/png")

if __name__ == '__main__':
    app.run()
