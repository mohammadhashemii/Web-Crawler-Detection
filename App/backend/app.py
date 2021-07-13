from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
##Cross-Origin Resource Sharing 

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/')
def getRoot():
    return "SALAAAM"

@app.route('/crawl', methods=['POST'])
@cross_origin()
def getIsCrawled():
    uploadedFile = request.files["file"]                    
    if uploadedFile:
        file_path = os.path.join(uploads_dir, uploadedFile.filename)
        uploadedFile.save(file_path)
        print(file_path)
        #print(uploadedFile.read())

        ##TODO convert to csv
    mockReturn = [["logloglog", 123], ["logloglog", 222], ["logloglog", 434], ["logloglog", 222], ["logloglog", 434], ["logloglog", 222], ["logloglog", 434], ["logloglog", 222], ["logloglog", 434], ["logloglog", 222], ["logloglog", 434], ["logloglog", 222], ["logloglog", 434]]
    return jsonify(mockReturn)

if __name__ == '__main__':
    app.run(debug=True, port=5005)