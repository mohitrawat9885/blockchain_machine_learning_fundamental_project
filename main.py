from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
from block import write_block, check_integrity

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        if not request.files['file']:
            return render_template('index.html')
        text = request.form.get('mytext')
        f = request.files['file']
        
        f.save(secure_filename(f.filename))
        myShapes =  getAllShapes(f.filename)
        print("All Shapes are", myShapes, "  Text ", text)

        for i in myShapes:
            write_block(shape=i, text=text)

    return render_template('index.html')


@app.route('/checking')
def check():
    results = check_integrity()
    return render_template('index.html', checking_results=results)



def getAllShapes(imgName):
    img = cv2.imread(imgName)
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh =cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
    contours,hierarchy=cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    shapes_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        if len(approx) == 3:
            shape_detected = "Triangle"
        elif len(approx) == 4:
            x1 ,y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                shape_detected = "Square"
            else:
                shape_detected = "Rectangle"
        elif len(approx) == 5:
            shape_detected = "Pentagon"

        elif len(approx) == 10:
            shape_detected = "Star"
        else:
            shape_detected = "Circle"
        shapes_list.append(shape_detected)

    return shapes_list








if __name__ == '__main__':
    app.run(debug=True)















