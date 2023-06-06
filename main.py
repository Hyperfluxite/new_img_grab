from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def process_image():
    url = request.args.get('url')
    
    if url is None:
        return jsonify(error='Missing URL parameter'), 400
    
    lua_table = image_to_lua_table(url)
    return jsonify(lua_table)

def image_to_lua_table(url):
    # Download the image from the URL
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    # Get image dimensions
    width, height = image.size

    # Create a Lua table to store pixel information
    lua_table = []

    # Iterate over each pixel and store its information
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            lua_table.append((x, y, *pixel))

    return lua_table

if __name__ == '__main__':
    app.run()
