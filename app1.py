from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image
import requests
import re

app = Flask(__name__)

@app.route('/<path:url>')
def convert_image(url):
    # Parse the remote URL and URI from the request
    match = re.match(r'(https?://[^/]+)(/.*)', url)
    remote_url, uri = match.groups()

    # Download the image from the remote URL
    response = requests.get(remote_url + uri)

    # Open the downloaded image with Pillow
    img = Image.open(BytesIO(response.content))

    # Get the resize dimensions from the request, defaulting to the original size
    resize = request.args.get('resize')
    if resize:
        width, height = [int(d) for d in resize.split('x')]
        img = img.resize((width, height))

    # Convert the image to WebP format
    webp_img = BytesIO()
    img.save(webp_img, 'webp')
    webp_img.seek(0)

    # Serve the converted image
    return send_file(webp_img, mimetype='image/webp')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

