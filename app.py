from flask import Flask, request, jsonify, render_template, Response
import requests
from collections import OrderedDict
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={
    r"/*": {"origins": "https://college-result-1phb.onrender.com"}
})

# ----------------- Backend functions -----------------
def get_student_data(scholarno):
    url = f"https://academic.manit.ac.in/api/StudentActivity/GetStudentData?scholarno={scholarno}"
    headers = {"Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def get_student_result(form_id):
    url = f"https://academic.manit.ac.in/api/StudentActivity/GetStudentResult?FormId={form_id}"
    headers = {"Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

# ----------------- Routes -----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch-student-result', methods=['POST'])
def fetch_student_result():
    try:
        data = request.json
        scholarno = data.get('scholarno')

        if not scholarno:
            return jsonify({"error": "Scholar number is required"}), 400

        student_data = get_student_data(scholarno)
        if not student_data:
            return jsonify({"error": "No student data found"}), 404

        form_id = student_data[0].get('FormId')
        if not form_id:
            return jsonify({"error": "FormId not found"}), 404

        # fetch all semester results in one go
        result_data = get_student_result(form_id)

        return jsonify(result_data)

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
@app.route('/fetch-pdf/<int:id>')
def fetch_pdf(id):
    try:
        url = f"https://academic.manit.ac.in/api/StudentActivity/GetMarkSheetPdf?Id={id}"
        headers = {"User-Agent": "Mozilla/5.0"}
        cookies = {
            "ASP.NET_SessionId": "nnaealoizmtpmc2da2zvbtxs",
            "StudentPanel": "userid=16362&Email=211112055&ScholarNo=211112055"
        }
        r = requests.get(url, headers=headers, cookies=cookies, verify=False)
        return Response(r.content, content_type='application/pdf')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True)
