import pytesseract        
from PIL import Image      

import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory

from werkzeug.utils import secure_filename

app=Flask(__name__)

UPLOAD_FOLDER ='static/uploads/'

app.config['SECRET_KEY'] = 'opencv'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024


#pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'   
#pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/share/tesseract-ocr/4.00/tessdata'


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


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
                
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                
                image_scan = Image.open(file)
                extracted_text = pytesseract.image_to_string(image_scan)
                image_list.append(filename)
                image_file_list.append(extracted_text)
        
        return render_template('upload.html',
                                   msg='Successfully processed',                                   
                                   image_info= zip(image_file_list, image_list))                               
    
if __name__ == "__main__":
    app.run(debug=True)
