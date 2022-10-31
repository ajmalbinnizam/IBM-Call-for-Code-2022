from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image

app = Flask(__name__)

dic = {0: 'lions', 1: 'elephant'}

# need to import tensorflow
model = load_model('saved_model.pb')
model.make_predict_function()


def predict_label(img_path):
    i = image.load_img(img_path, target_size=(100, 100))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 100, 100, 3)
    p = model.predict_classes(i)
    return dic[p[0]]


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")


@app.route("/about")
def about_page():
    return ""


@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/" + img.filename
        img.save(img_path)
        if request.region_selected == "region 1":
            img_path = "model/All_Regions/Region 1/" + img.filename
            img.save(img_path)
        else:
            img_path = "model/All_Regions/Region 2/" + img.filename
            img.save(img_path)
        # p = predict_label(img_path)
    # render_template("index.html", prediction = p, img_path = img_path)
    return render_template("submit.html", message="File uploaded")
# return render_template("status.html")


if __name__ == '__main__':
    #app.debug = True
    app.run(debug=True)
