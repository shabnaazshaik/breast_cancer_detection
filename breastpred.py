ACfrom flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Load the trained model
model = load_model('C:\\Users\\saivi\\AppData\\Local\\Programs\\Python\\Python310\\breast_cancer_classification_model.h5')  # Update with the path to your saved model

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # If the user does not select a file, browser also submits an empty part without filename
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Check if the file has the allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Save the file to the static folder
            file_path = os.path.join('static', filename)
            file.save(file_path)

            # Make a prediction on the uploaded image
            prediction = predict_image(file_path)

            # Render the home page with the uploaded image and prediction
            return render_template('index.html', filename=filename, prediction=prediction)

        return render_template('index.html', error='Invalid file format. Please upload a valid image.')

    return render_template('index.html')

# Function to make a prediction on the uploaded image
def predict_image(file_path):
    img = image.load_img(file_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Make the prediction
    prediction = model.predict(img_array)

    if prediction[0][0] > 0.5:
        return 'Malignant'
    else:
        return 'Benign'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
