
import os
from flask import Flask, request, render_template, send_from_directory,flash

from pylab import *




app=Flask(__name__)
app.secret_key='random string'

classes=['Crashed','Normal']


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")
@app.route('/upload1/<filename>')
def send_image(filename):
    print('kjsifhuissywudhj')
    return send_from_directory("images", filename)

@app.route("/upload1", methods=["POST","GET"])
def upload1():
    print('a')
    if request.method=='POST':
        myfile = request.files['file']
        print("sdgfsdgfdf")
        fn = myfile.filename
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)

        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)
        # import tensorflow as tf
        import numpy as np
        from tensorflow.keras.preprocessing import image
        from tensorflow.keras.models import load_model
        # img = r"D:\Fathima\Python\medical image\database\train\Eye\006.jpg"
        new_model = load_model("visualizations/FinalModel.h5")
        test_image = image.load_img(mypath, target_size=(224,224))
        test_image = image.img_to_array(test_image)
        print(test_image)
        test_image = test_image / 255
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)

        prediction = classes[np.argmax(result)]

        if prediction=='Crashed':
            import requests

            url = "https://www.fast2sms.com/dev/bulkV2"

            message = 'Alert!!!! Car is crashed'
            no = ""
            data = {
                "route": "q",
                "message": message,
                "language": "english",
                "flash": 0,
                "numbers": no,
            }

            headers = {
                "authorization": "IST0gV8v69pFKzWeXDanQtPlboBAGwLk5hNRZcryOuiC7UjM2xQMzJgjplbUPXOeFDoyicSLZfIB61mT",
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, json=data)
            print(response)
        else:
            print('normal')



    return render_template("template.html", image_name=fn, text=prediction)




if __name__=='__main__':
    app.run(debug=True)

