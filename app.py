from flask import Flask, flash, request, send_from_directory, redirect
from flask import Flask, flash, request, redirect, url_for
import os
from flask import jsonify
import base64

from pyzbar.pyzbar import decode
from PIL import Image


UPLOAD_FOLDER = './output/'

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='', static_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

#########################
## home
# GET:  Return index.html
# POST: Typical form POST with redirect as response
#########################
@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
	    return app.send_static_file('index.html')


    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files: 
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = "123" + file.filename 
            print("Saving to " +  filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            # Decode bar
            output = decode(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            print("output" , output)
            code = b''
            for item in output:
                print("code --> ", item.data)
                code = item.data


            # Redirect to home            
            return redirect('/?code='+code.decode() )
            #return jsonify({'message': 'ok'})


#########################
## upload
# POST: upload with base64 POST JSON
#########################
@app.route('/upload/base64/', methods=['GET','POST'])
def upload_base64():
    if request.method == "POST":
        print("Setting test in here")
        content = request.json
        img_b64 = content['data_url']
        img_b64 = img_b64.replace('data:image/png;base64,','')
        imgdata = base64.b64decode(img_b64)
        filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        
        # Decode bar
        output = decode(Image.open('capture.jpg'))
        print(output)
        code = ''
        for item in output:
            print("code --> ", item.data)
            code = item.data

        return jsonify({'message': 'ok', 'code': code})

@app.route('/form/', methods=['GET','POST'])
def upload_form():
    if request.method == "POST":
        image_file = request.form['file']
        image_file.save(image_file.filename)
        return redirect('/')

@app.route('/form/ajax/', methods=['GET','POST'])
def upload_form_ajax():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files: 
            flash('No file part')
            return jsonify({'message': 'failed - no file part'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({'message': 'failed - no selected file'})
        if file:
            filename = "123" + file.filename 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Decode bar
            output = decode(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            code_list = []
            for item in output:
                code_list.append( item.data.decode() ) 

            # Redirect to home            
            return jsonify({'message': 'ok', 'code_list': code_list })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
