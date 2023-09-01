from flask import Flask, request, render_template, flash, redirect, url_for, send_file
from os import listdir, path, remove, mkdir
from io import BytesIO
# from werkzeug import secure_filename

app = Flask(__name__)

if not path.exists('uploads'):
    mkdir('uploads')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'random key here'


@app.route('/')
def index():
    uploaded_files = listdir('uploads')
    print(uploaded_files)
    return render_template('upload.html', uploaded_files=uploaded_files)


@app.route('/uploader', methods=['POST'])
def upload_handler():
    f = request.files['file']
    # print(request.files)
    f.save(path.join(app.config['UPLOAD_FOLDER'], f.filename))
    flash('file Uploaded Successfully', 'info')
    return redirect(url_for('index'))


@app.route('/download/<path:filename>')
def download_file(filename):
    if filename in listdir('uploads'):
        file = path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file, download_name=filename, as_attachment=True)
    flash('File not found. Cannot download file')
    return redirect(url_for('index'))


@app.route('/delete/<path:filename>')
def delete_file(filename):
    if filename in listdir('uploads'):
        remove(path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'file "{filename}" deleted successfully', 'info')
    flash('file not found')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
