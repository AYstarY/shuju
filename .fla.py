from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置上传文件的目标路径
UPLOAD_FOLDER = '/storage/emulated/0/Python/网站1.0/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件被上传
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        # 如果用户没有选择文件，则浏览器也会提交一个空的部分，没有文件名
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"File {filename} uploaded successfully!"
        else:
            return "Invalid file type!"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5010)