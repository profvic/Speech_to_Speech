from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import os
from pathlib import Path
# Flask App Configuration
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dictionary to store audio files by category
audio_files = {}

@app.route("/")
def index():
    """Render the upload/record page."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    """Handle audio file uploads."""
    category = request.form.get("category")
    file = request.files.get("audio")

    if not category or not file:
        return jsonify({"error": "Category and file are required!"}), 400
    
    ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "webm"}
    if not file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported audio format!"}), 400

    # Create category folder if it doesn't exist
    category_folder = os.path.join(app.config["UPLOAD_FOLDER"], category)
    os.makedirs(category_folder, exist_ok=True)

    # Save the file
    file_path = os.path.join(category_folder, file.filename)
    file.save(file_path)

    # Update the dictionary
    if category not in audio_files:
        audio_files[category] = []
    unix_style_path = Path(file_path).as_posix()
    audio_files[category].append(f"/{unix_style_path}")  # Use Unix-style path for URLs

    return redirect(url_for("view_audio_clips"))

@app.route("/audio_clips")
def view_audio_clips():
    """Render the page displaying categorized audio clips."""
    return render_template("audio_clips.html", audio_files=audio_files)

@app.route("/static/uploads/<path:filename>")
def serve_audio(filename):
    """Serve uploaded audio files."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
