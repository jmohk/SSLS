import csv
from flask import Flask, Response, request, render_template, jsonify
import model
import cv2

app = Flask(__name__)

num_faces_detected = 0

# Define sunrise and sunset times for each month
timetable = {
    1: {"sunrise": 6.50, "sunset": 17.17},
    2: {"sunrise": 6.34, "sunset": 17.44},
    3: {"sunrise": 6.03, "sunset": 18.04},
    4: {"sunrise": 5.26, "sunset": 18.23},
    5: {"sunrise": 5.59, "sunset": 19.42},
    6: {"sunrise": 5.52, "sunset": 19.59},
    7: {"sunrise": 6.02, "sunset": 19.59},
    8: {"sunrise": 6.21, "sunset": 19.37},
    9: {"sunrise": 6.38, "sunset": 19.01},
    10: {"sunrise": 6.56, "sunset": 18.25},
    11: {"sunrise": 6.19, "sunset": 17.00},
    12: {"sunrise": 6.42, "sunset": 16.58}
}

def calculate_light_decision(hour, month):
    sunrise = timetable[month]["sunrise"]
    sunset = timetable[month]["sunset"]
    if sunrise <= hour < sunset:
        return "Turn on 0% of light bulbs"
    else:
        return "Turn on 100% of light bulbs"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.json

        if 'values' in data and isinstance(data['values'], list):
            integer_list = data['values']
            print(integer_list)
            model.save_to_csv(integer_list, 'test.csv')
            model.run()

        light_result = model.get_light("decoded_result.csv")
        prediction_result = "Some prediction result"  # Replace this with your actual prediction logic
        
        return jsonify({"prediction": prediction_result, "optimalLight": light_result})

    return render_template("index.html")

@app.route("/form-1", methods=['POST', 'GET'])
def form1():
    if request.method == 'POST':
        # Handle form-1 submission here
        data = request.json
        if 'values' in data and isinstance(data['values'], list):
            integer_list = data['values']
            print(integer_list)
            model.save_to_csv(integer_list, 'test.csv')
            model.run()

        light_result = model.get_light("decoded_result.csv")
        prediction_result = "Some prediction result"  # Replace this with your actual prediction logic
        
        return jsonify({"prediction": prediction_result, "optimalLight": light_result})
    
    return render_template("index.html")

@app.route("/form-2", methods=['POST', 'GET'])
def form2():
    global hour, month
    if request.method == 'POST':
        # Handle form-2 submission here
        data = request.json
        if 'hour' in data and 'month' in data:
            hour = int(data['hour'])
            month = int(data['month'])
            light_decision = calculate_light_decision(hour, month)
            return jsonify({"light_decision": light_decision})
    
    return render_template("index.html")

def detect_faces(frame):
    global num_faces_detected
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        num_faces_detected = len(faces)
        return num_faces_detected
    except Exception as e:
        print("Error detecting faces:", e)
        return 0

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            num_faces = detect_faces(frame)
            cv2.putText(frame, f'Number of Faces: {num_faces}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/num_faces')
def num_faces():
    global num_faces_detected
    try:
        return str(num_faces_detected)
    except Exception as e:
        print("Error returning number of faces:", e)
        return "0"

def get_second_row_first_column(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there's one
        second_row = next(reader, None)
        if second_row:
            return second_row[0]  # Assuming you want the first column of the second row
    return None

@app.route('/chart_data')
def chart_data():
    global month, hour
    b = 0
    light_result = 0  # Define light_result here or retrieve it from where it's defined
    if month in timetable and hour is not None:
        if calculate_light_decision(hour, month) == "Turn on 100% of light bulbs":
            b = 100
    a = get_second_row_first_column("decoded_result.csv")
    data = {"a": a, "b": b}  # Prepare data for JSON response
    return jsonify(data)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == "__main__":
    app.run(debug=True)
