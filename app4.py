from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image
import requests
import re

app = Flask(__name__)

@app.route('/resize/<int:width>x<int:height>/<path:url>')
def resize_image(width, height, url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    remote_url, uri = match.groups()

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the file format is JPEG
    if response.headers['content-type'] != 'image/jpeg':
        return send_file(BytesIO(response.content), mimetype=response.headers['content-type'])

    # Open the downloaded image with Pillow
    img = Image.open(BytesIO(response.content))

    # Resize the image to the requested dimensions
    img = img.resize((width, height))

    # Serve the resized image
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/webp/<path:url>')
def convert_to_webp(url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    remote_url, uri = match.groups()

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the file format is JPEG
    if response.headers['content-type'] != 'image/jpeg':
        return send_file(BytesIO(response.content), mimetype=response.headers['content-type'])

    # Open the downloaded image with Pillow
    img = Image.open(BytesIO(response.content))

    # Convert the image to WebP format
    webp_img = BytesIO()
    img.save(webp_img, 'webp')
    webp_img.seek(0)

    # Serve the converted image
    return send_file(webp_img, mimetype='image/webp')

@app.route('/webp/<int:width>x<int:height>/<path:url>')
def resize_and_convert_to_webp(width, height, url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    remote_url, uri = match.groups()

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the file format is JPEG
    if response.headers['content-type'] != 'image/jpeg':
        return send_file(BytesIO(response.content), mimetype=response.headers['content-type'])

    # Open the downloaded image with Pillow
    img = Image.open(BytesIO(response.content))

    # Resize the image to the requested dimensions
    img = img.resize((width, height))

    # Convert the image to WebP format
    webp_img = BytesIO()
    img.save(webp_img, 'webp')
    webp_img.seek(0)

    # Serve the converted image
    return send_file(webp_img, mimetype='image/webp')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

