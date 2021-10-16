import pytesseract        
from PIL import Image      

import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'   
        


# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            
            
            return render_template('upload.html', msg='No file selected')

        files = request.files.getlist('file')
        
        
        image_list = [] 
        image_file_list = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                
                extracted_text = pytesseract.image_to_string(Image.open(filename))
                image_list.append(filename)
                image_file_list.append(extracted_text)
        
        return render_template('upload.html',
                                   msg='Successfully processed',                                   
                                   image_info= zip(image_file_list, image_list),
                                   img_src=UPLOAD_FOLDER + file.filename)
    
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)
