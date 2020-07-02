from flask import g
import os
# from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, make_response, template_rendered, session
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import urllib.parse
import json
from bson import json_util, ObjectId
import requests
import csv
from imageai.Prediction.Custom import CustomImagePrediction
import FirstCustomImageRecognition
import operator
import gc
import pprint
from pympler.tracker import SummaryTracker


from flask import Flask


tracker = SummaryTracker()


# Garbage collection
# Force a sweep
print('Collecting')
gc.collect()
print('Done')

# print('Remaining Garbage:')
# pprint.pprint(gc.garbage)


# folder for testing
UPLOAD_FOLDER = 'static/uploads/'


# # Create an instance of Flask
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# # ===========================================
# # Connect to MongoDB Atlas
# username = urllib.parse.quote_plus('mongo')
# password = urllib.parse.quote_plus('mongo')
# client = MongoClient(
#     'mongodb+srv://%s:%s@cluster0-8yire.mongodb.net/test?retryWrites=true&w=majority' % (username, password))

# # Connect to the "art" MongoDB Atlas database
# db = client.art
# facts = db.art.find_one()


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# home page
@app.route('/')
def upload_form():

    # Return template and data
    return render_template("upload.html")


# image upload
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        # flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        # flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)

        # flash('Image successfully uploaded and displayed')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


# image display
@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


# image_recognition function
@app.route("/image_recognition/<filename>")
def img_recognition(filename):
    predictions = None
    g.predictions = None

    # print('display_image filename: ' + filename)
    testing_image = 'static/uploads/' + filename

    # Run the image_recognition function
    predictions = FirstCustomImageRecognition.image_recognition(testing_image)
    # print(predictions)

    g.predictions = predictions
    # return g.predictions

    # sort a predictions dictionary
    sorted_p = sorted(predictions.items(), key=operator.itemgetter(1))
    best_prediction = sorted_p[-1]
    # print(sorted_p)
    # print(best_prediction)
    # print(best_prediction[0])

    with open('Top10Artists.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        artists = []

        for row in data:
            if not first_line:
                if row[0] == best_prediction[0]:
                    artists.append({
                        "artist": row[0],
                        "info": row[1],
                        "url": row[2]
                    })

            else:
                first_line = False
        # print(artists)
        # return render_template("index.html", places=places)

    # Delete filename from uploaded folder
    # print('delete files from folder')
    # print('Filename: ', filename)
    # print('Folder name: ', app.config['UPLOAD_FOLDER'])

    # get list of files in the directory
    files_in_dir = os.listdir(app.config['UPLOAD_FOLDER'])

    # loop to delete each file in folder
    for f in files_in_dir:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

    # Remove Folder
    # import shutil
    # shutil.rmtree(app.config['UPLOAD_FOLDER'])

    tracker.print_diff()
    # Clear references held by gc.garbage

    print('Clearing gc.garbage:')
    del gc.garbage[:]

    # Everything should have been freed this time
    # print('Collecting')
    # gc.collect()
    # print('Done')

    # print('Remaining Garbage:')
    # pprint.pprint(gc.garbage)

    # Redirect back to home page
    return render_template("upload.html", predictions=g.predictions, filename=filename, artists=artists)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
