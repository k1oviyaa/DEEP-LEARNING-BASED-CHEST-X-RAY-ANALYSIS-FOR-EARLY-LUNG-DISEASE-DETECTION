from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model
from flask import Blueprint, request, url_for, render_template
from werkzeug.utils import secure_filename
import os

import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

from flask import Flask
app = Flask(__name__)


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
plt.switch_backend('agg')

views = Blueprint("views", __name__)

# Load your saved model
model = load_model('vgg_capsule.h5')

# Define the prediction function
import uuid

def predict_save(img):
    class_names = ['Bacterial Pneumonia', 'Corona Virus Disease', 'Normal', 'Viral Pneumonia', 'Lung Cancer']

    my_image = load_img(img, target_size=(128, 128))  # Resize to model's input
    my_image = img_to_array(my_image)
    my_image = np.expand_dims(my_image, axis=0)

    out = np.round(model.predict(my_image)[0], 2)

    # Generate a unique filename
    pred_img_filename = f"pred_img.png"
    pred_img_path = os.path.join("static", pred_img_filename)

    # Create and save the bar chart
    fig = plt.figure(figsize=(7, 4))
    plt.barh(class_names, out, color='lightgray', edgecolor='red', linewidth=1, height=0.5)

    for index, value in enumerate(out):
        plt.text(value / 2 + 0.1, index, f"{100 * value:.2f}%", fontweight='bold')

    plt.xticks([])
    plt.yticks(range(len(class_names)), labels=class_names, fontweight='bold', fontsize=14)

    fig.savefig("./static/pred_img.png", bbox_inches='tight')
    plt.close(fig)  # Close the figure to release memory

    return pred_img_filename  # Return only the filename



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        file = request.files['file']
        if file:
            input_img = secure_filename(file.filename)
            file_path = os.path.join("./static/uploads", input_img)
            file.save(file_path)

            pred_img_path = predict_save(file_path)  # Get prediction image path
            return render_template('home.html', input_img=input_img, pred_img=pred_img_path)

    return render_template('home.html', input_img=None, pred_img=None)


@app.route('/about')
def about():
    return render_template('about.html')



# main
if __name__ == "__main__":
    app.run()