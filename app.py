from flask import Flask, render_template, request, jsonify
from rembg import remove
import io
import base64
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_image():
    """API endpoint to process and remove background"""
    try:
       
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not file.filename.lower().endswith(('jpg', 'jpeg', 'png')):
            return jsonify({'error': 'Only JPG and PNG files are supported'}), 400
        
        print(f"Processing image: {file.filename}")
        
        # Open the image
        img = Image.open(file.stream)
        print(f"Original image size: {img.size}")
        
        # Remove background using rembg
        output = remove(img)
        print("Background removed successfully")
        
        # Convert to base64 for sending to frontend
        img_io = io.BytesIO()
        output.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Encode as base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'filename': file.filename
        })
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)