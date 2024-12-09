from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/convertimagetotext', methods=['GET'])
def get_image_pixels():
    # Get the image URL from the request's query parameter
    image_url = request.args.get('link')
    
    if not image_url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for invalid responses
        
        # Open the image using PIL
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")  # Ensure the image is in RGB mode
        
        # Initialize an empty list to store the pixel data
        pixels = []
        
        # Loop through all pixels and get the RGB values
        width, height = img.size
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))  # Get RGB values at (x, y)
                pixels.append({"x": x, "y": y, "rgb": {"r": r, "g": g, "b": b}})
        
        # Return the pixel data as JSON
        return jsonify({"pixels": pixels})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to process image", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
