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
allowed_domains = {domain.strip() for domain in config.get('app', 'allowed_domains').split(',')}

@app.route('/<int:width>x<int:height>/<path:url>')
def resize_image(width, height, url):
    # Validate input values
    if width < 0 or height < 0:
        return 'Invalid input', 400

    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    if not match:
        return 'Invalid URL', 400
    remote_url, uri = match.groups()

    # Check if the remote URL domain is in the allowed domains list
    if not any(domain in remote_url for domain in allowed_domains):
        return 'Access denied', 403

    # Check if the file format is JPEG, PNG, or WEBP
    try:
        response = requests.get(remote_url + uri, stream=True)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        content_type = response.headers.get('content-type', '')
        if not (content_type.startswith('image/jpeg') or content_type.startswith('image/png') or content_type.startswith('image/webp')):
            return send_file(BytesIO(response.content), mimetype=content_type)
    except requests.exceptions.RequestException as e:
        return 'Error retrieving image: ' + str(e), 500

    # Open the downloaded image with PIL
    try:
        with Image.open(BytesIO(response.content)) as img:
            # Calculate the new width and height based on the aspect ratio of the original image
            img_width, img_height = img.size
            if width == 0:
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
            if content_type.startswith('image/jpeg'):
                img.save(img_io, 'JPEG')
            elif content_type.startswith('image/png'):
                img.save(img_io, 'PNG')
            elif content_type.startswith('image/webp'):
                img.save(img_io, 'WEBP')
            else:
                return send_file(BytesIO(response.content), mimetype=content_type)
            img_io.seek(0)
            return send_file(img_io, mimetype=content_type)
    except OSError as e:
        return 'Error processing image: ' + str(e), 500
    except ValueError as e:
        return 'Error processing image: ' + str(e), 500

@app.route('/webp/<path:url>')
def convert_to_webp(url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    if not match:
        return 'Invalid URL', 400
    remote_url, uri = match.groups()

    # Check if the remote URL domain is in the allowed domains list
    if not any(domain in remote_url for domain in allowed_domains):
        return 'Access denied', 403

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Check if the response was successful
    if response.status_code != 200:
        return 'Failed to download image', 500

    # Check if the file format is JPEG or PNG
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/jpeg') and not content_type.startswith('image/png'):
        return send_file(BytesIO(response.content), mimetype=content_type)

    # Open the downloaded image with Pillow
    try:
        img = Image.open(BytesIO(response.content))
    except:
        return 'Failed to open image', 500

    # Convert the image to WebP format
    webp_img = BytesIO()
    try:
        img.save(webp_img, 'webp')
    except:
        return 'Failed to convert image to WebP', 500
    webp_img.seek(0)

    # Serve the converted image
    return send_file(webp_img, mimetype='image/webp')

@app.route('/webp/<int:width>x<int:height>/<path:url>')
def resize_and_convert_to_webp(width, height, url):
    # Extract the remote URL and URI from the request URL
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    if not match:
        return 'Invalid URL', 400
    remote_url, uri = match.groups()

    # Check if the remote URL domain is in the allowed domains list
    if not any(domain in remote_url for domain in allowed_domains):
        return 'Access denied', 403

    # Download the image from the remote URL
    try:
        response = requests.get(remote_url + uri)
    except requests.exceptions.RequestException as e:
        return f'Error: {e}', 500

    # Check if the file format is JPEG, PNG, or WebP
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith(('image/jpeg', 'image/png', 'image/webp')):
        # Return the original file if it's not JPEG, PNG, or WebP
        return send_file(BytesIO(response.content), mimetype=content_type)

    # Open the downloaded image with Pillow
    try:
        img = Image.open(BytesIO(response.content))
    except OSError as e:
        return f'Error: {e}', 500

    # If the image format is already WebP, return it as-is
    if content_type == 'image/webp':
        return send_file(BytesIO(response.content), mimetype=content_type)

    # Calculate the new width and height based on the aspect ratio of the original image
    orig_width, orig_height = img.size
    if width == 0 and height == 0:
        # Return the original file if both width and height are 0
        return send_file(BytesIO(response.content), mimetype=content_type)
    elif width == 0:
        new_width = int(orig_width * height / orig_height)
        new_height = height
    elif height == 0:
        new_width = width
        new_height = int(orig_height * width / orig_width)
    else:
        new_width = width
        new_height = height

    # Resize the image to the requested dimensions
    img = img.resize((new_width, new_height), resample=Image.LANCZOS)

    # Convert the image to WebP format
    webp_img = BytesIO()
    img.save(webp_img, 'webp', quality=85)
    webp_img.seek(0)

    # Serve the converted image
    return send_file(webp_img, mimetype='image/webp')

if __name__ == '__main__':
    app.run(debug=True, port=5001, threaded=True)
    #app.run(port=5001, threaded=True)


