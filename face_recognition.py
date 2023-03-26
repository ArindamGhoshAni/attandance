from flask import Flask, render_template
from threading import Thread

app = Flask(_name_)

def run_recognition():
    recognize_faces()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_camera')
def start_camera():
    t = Thread(target=run_recognition)
    t.start()
    return 'Camera started'

@app.route('/take_attendance')
def take_attendance():
    # Read attendance file and return as response
    with open(attendance_file, 'r') as csvfile:
        data = csvfile.read()
    return data

if _name_ == '_main_':
    app.run(debug=True)
