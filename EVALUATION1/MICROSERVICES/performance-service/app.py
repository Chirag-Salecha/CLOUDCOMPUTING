from flask import Flask, jsonify

app = Flask(__name__)

performance = {
    101: {
        "student_id": 101,
        "cgpa": 8.7,
        "grade": "A"
    },
    102: {
        "student_id": 102,
        "cgpa": 9.1,
        "grade": "A+"
    }
}


@app.route("/")
def home():
    return jsonify({
        "service": "Performance Service",
        "status": "running"
    })


@app.route("/performance/<int:student_id>")
def get_performance(student_id):
    record = performance.get(student_id)

    if record:
        return jsonify(record)

    return jsonify({
        "error": "Performance record not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)