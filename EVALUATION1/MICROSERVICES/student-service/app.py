from flask import Flask, jsonify
import requests

app = Flask(__name__)

students = {
    101: {
        "id": 101,
        "name": "Chirag Salecha",
        "branch": "CSE-AI",
        "semester": 5
    },
    102: {
        "id": 102,
        "name": "Rahul Sharma",
        "branch": "CSE-AI",
        "semester": 5
    }
}


@app.route("/")
def home():
    return jsonify({
        "service": "Student Service",
        "status": "running"
    })


@app.route("/students")
def get_students():
    return jsonify(list(students.values()))


@app.route("/students/<int:student_id>")
def get_student(student_id):
    student = students.get(student_id)

    if student:
        return jsonify(student)

    return jsonify({
        "error": "Student not found"
    }), 404


@app.route("/student-summary/<int:student_id>")
def student_summary(student_id):

    student = students.get(student_id)

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    try:
        attendance_response = requests.get(
            f"http://attendance-service:5000/attendance/{student_id}",
            timeout=5
        )

        performance_response = requests.get(
            f"http://performance-service:5000/performance/{student_id}",
            timeout=5
        )

        attendance_response.raise_for_status()
        performance_response.raise_for_status()

        attendance = attendance_response.json()
        performance = performance_response.json()

        return jsonify({
            "student": student,
            "attendance": attendance,
            "performance": performance
        })

    except requests.RequestException as e:
        return jsonify({
            "error": "Failed to communicate with another service",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)