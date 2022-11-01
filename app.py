from flask import Flask, render_template, request
# from keras.models import load_model
# from keras.preprocessing import image
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv) 
import os
import cv2
import tensorflow as tf
from tensorflow import keras
import joblib
app = Flask(__name__)


model= keras.models.load_model(r"./model")
label_encoder = joblib.load(r"./label_encoder.joblib")

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")


@app.route("/submit", methods=['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		# img = request.files['my_image']
		# img_path = "static/" + img.filename
		# img.save(img_path)
		# if(request.region_selected == "region 1"):
		# 	img_path = "model/All_Regions/Region 1/" + img.filename
		# 	img.save(img_path)
		# else:
		# 	img_path = "model/All_Regions/Region 2/" + img.filename
		# 	img.save(img_path)

		All_Region_dir = request.form['add_info']
		
		finaldf=pd.DataFrame(columns=['Image_Name','Region_Name','Species'])
		for i in range(0,len(os.listdir(All_Region_dir))):
			region_dir=All_Region_dir+'\\'+os.listdir(All_Region_dir)[i]
			preds=animal_identifier(region_dir)
			finaldf=finaldf.append(preds,ignore_index=True)
			finaldf.to_csv('Region_Wise_Predictions.csv',index=False)

		# p = predict_label(img_path)
        # render_template("index.html", prediction = p, img_path = img_path)
		return render_template("submit.html", message = All_Region_dir)

def animal_identifier(region_dir):
    df=pd.DataFrame(columns=['Image_Name','Region_Name','Species'])
    for i in range(0,len(os.listdir(region_dir))):
        images=[]
        img = cv2.imread(region_dir+'/'+os.listdir(region_dir)[i])
        resized_img = cv2.resize(img,(224,224))
        resized_img = resized_img / 255.0
        images.append(resized_img)
        images = np.array(images,dtype = 'float32')
        preds = model.predict(images)
        preds = np.argmax(preds,axis = 1)
        pred_animal=label_encoder.inverse_transform([preds[0]])[0]
        df.loc[i,'Image_Name']=os.listdir(region_dir)[i]
        df.loc[i,'Region_Name']=region_dir.split('\\')[-1]
        df.loc[i,'Species']=pred_animal
    return df

if __name__ == '__main__':
    #app.debug = True
    app.run(debug=True)
