from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image
import requests
import re
import configparser
import threading

app = Flask(__name__)

# Read allowed domains from config file
config = configparser.ConfigParser()
config.read('config.ini')
allowed_domains = [domain.strip() for domain in config.get('app', 'allowed_domains').split(',')]

@app.route('/<int:width>x<int:height>/<path:url>')
def resize_image(width, height, url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    remote_url, uri = match.groups()

    # Check if the remote URL domain is in the allowed domains list
    if not any(domain in remote_url for domain in allowed_domains):
        return 'Access denied', 403

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the file format is JPEG or PNG
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/jpeg') and not content_type.startswith('image/png'):
        return send_file(BytesIO(response.content), mimetype=content_type)

    # Open the downloaded image with Pillow
    img = Image.open(BytesIO(response.content))

    # Calculate the new width and height based on the aspect ratio of the original image
    img_width, img_height = img.size
    if width == 0 and height == 0:
        return send_file(BytesIO(response.content), mimetype=content_type)
    elif width == 0:
        new_width = int(img_width * height / img_height)
        new_height = height
    elif height == 0:
        new_width = width
        new_height = int(img_height * width / img_width)
    else:
        new_width = width
        new_height = height

    # Resize the image to the requested dimensions
    img = img.resize((new_width, new_height))

    # Serve the resized image
    img_io = BytesIO()
    img.save(img_io, 'JPEG' if content_type.startswith('image/jpeg') else 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype=content_type)


@app.route('/webp/<path:url>')
def convert_to_webp(url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    remote_url, uri = match.groups()

    # Check if the remote URL domain is in the allowed domains list
    if not any(domain in remote_url for domain in allowed_domains):
        return 'Access denied', 403

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the file format is JPEG or PNG
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/jpeg') and not content_type.startswith('image/png'):
        return send_file(BytesIO(response.content), mimetype=content_type)

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

    # Check if the remote URL domain is in the allowed domains list
    if not any(domain in remote_url for domain in allowed_domains):
        return 'Access denied', 403

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the file format is JPEG or PNG
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/jpeg') and not content_type.startswith('image/png'):
        return send_file(BytesIO(response.content), mimetype=content_type)

    # Open the downloaded image with Pillow
    img = Image.open(BytesIO(response.content))

    # Calculate the new width and height based on the aspect ratio of the original image
    img_width, img_height = img.size
    if width == 0 and height == 0:
        return send_file(BytesIO(response.content), mimetype=content_type)
    elif width == 0:
        new_width = int(img_width * height / img_height)
        new_height = height
    elif height == 0:
        new_width = width
        new_height = int(img_height * width / img_width)
    else:
        new_width = width
        new_height = height

    # Resize the image to the requested dimensions
    img = img.resize((new_width, new_height))

    # Convert the image to WebP format
    webp_img = BytesIO()
    img.save(webp_img, 'webp')
    webp_img.seek(0)

    # Serve the converted image
    return send_file(webp_img, mimetype='image/webp')


if __name__ == '__main__':
	app.run(debug=True, port=5001, threaded=True)


