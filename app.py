import os
from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/convertimagetotext', methods=['GET'])
def get_image_pixels():
    image_url = request.args.get('link')
    if not image_url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        pixels = [{"x": x, "y": y, "rgb": dict(zip("rgb", img.getpixel((x, y))))}
                  for y in range(img.height) for x in range(img.width)]
        return jsonify({"pixels": pixels})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to process image", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT variable, default to 5000
    app.run(host='0.0.0.0', port=port)
