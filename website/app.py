from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Process CSV (dummy pass-through)
        df = pd.read_csv(file_path)
        processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}")
        df.to_csv(processed_path, index=False)

        # Convert DataFrame to HTML table for preview
        table_html = df.to_html(classes='csv-preview', index=False)

        return render_template('preview.html', table=table_html, filename=f"processed_{file.filename}")

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)