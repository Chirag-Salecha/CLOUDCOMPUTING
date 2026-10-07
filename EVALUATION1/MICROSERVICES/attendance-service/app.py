from flask import Flask, jsonify

app = Flask(__name__)

attendance = {
    101: {
        "student_id": 101,
        "attendance_percentage": 87
    },
    102: {
        "student_id": 102,
        "attendance_percentage": 92
    }
}


@app.route("/")
def home():
    return jsonify({
        "service": "Attendance Service",
        "status": "running"
    })


@app.route("/attendance/<int:student_id>")
def get_attendance(student_id):
    record = attendance.get(student_id)

    if record:
        return jsonify(record)

    return jsonify({
        "error": "Attendance record not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)