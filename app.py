from flask import Flask, flash, request, send_from_directory
from flask import Flask, flash, request, redirect, url_for
import os
from flask import jsonify
import base64




UPLOAD_FOLDER = '.'

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='', static_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
	    return app.send_static_file('index.html')
    if request.method == "POST":
        print("MyTest")
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
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message': 'ok'})

@app.route('/upload/', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        print("Setting test in here")
        content = request.json
        print(content)
        img_b64 = content['data_url']
        img_b64 = img_b64.replace('data:image/png;base64,','')
        imgdata = base64.b64decode(img_b64)
        filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        
        return jsonify({'message': 'ok'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
