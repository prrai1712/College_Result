from flask import Flask, request, jsonify, render_template, Response
import requests
from collections import OrderedDict
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ----------------- Backend functions -----------------

def get_student_data(scholarno):
    url = f"https://academic.manit.ac.in/api/StudentActivity/GetStudentData?scholarno={scholarno}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def get_student_result(form_id):
    url = f"https://academic.manit.ac.in/api/StudentActivity/GetStudentResult?FormId={form_id}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

# ----------------- Routes -----------------

@app.route('/')
def home():
    return render_template('index.html')  # Serve frontend

@app.route('/fetch-student-result', methods=['POST'])
def fetch_student_result():
    try:
        data = request.json
        scholarno = data.get('scholarno')
        sem = data.get('semester')

        if not scholarno:
            return jsonify({"error": "Scholar number is required"}), 400

        student_data = get_student_data(scholarno)
        form_id = student_data[0].get('FormId')  # Adjust if API structure differs
        if not form_id:
            return jsonify({"error": "FormId not found"}), 404

        result_data = get_student_result(form_id)
        result_data = result_data[sem-1]  # Get semester-specific data

        ordered_response = OrderedDict([
            ("scholar_no", result_data.get("ScholarNo")),
            ("semester", result_data.get("Semester")),
            ("Name", result_data.get("StudentName")),
            ("Result", result_data.get("Result")),
            ("Obtained", result_data.get("ObtainGrandTotal")),
            ("Total", result_data.get("MaxGrandTotal")),
            ("SGPA", result_data.get("SGPA")),
            ("CGPA", result_data.get("CGPA")),
            ("Percentage", result_data.get("Percentage")),
        ])

        return Response(json.dumps(ordered_response), mimetype='application/json')

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# ----------------- Run App -----------------

if __name__ == '__main__':
    app.run(debug=True)
