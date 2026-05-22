import os
from flask import Flask, request, render_template
from anomaly_detection.detector import AnomalyDetector

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    user_config = {
        "idle_gap": {
            "threshold_seconds": float(request.form.get("threshold_seconds", 86400)),
            "housewide_window_minutes": float(request.form.get("housewide_window_minutes", 1440)),
            "housewide_sensor_ratio": float(request.form.get("housewide_sensor_ratio", 0.8)),
            "return_window_minutes": float(request.form.get("return_window_minutes", 60)),
            "return_sensor_ratio": float(request.form.get("return_sensor_ratio", 0.3)),
        }
    }

    detector = AnomalyDetector(filepath)
    detector.configure(user_config)
    results = detector.analyze()

    housewide = results["housewide_silences"]
    idle_gaps = results["idle_gaps"]
    absent = results["absent_firing"]

    return render_template("index.html",
        housewide=housewide.to_dict("records") if not housewide.empty else [],
        idle_gaps=idle_gaps.drop(columns=["idle_seconds"], errors="ignore").to_dict("records") if not idle_gaps.empty else [],
        absent=absent.to_dict("records") if not absent.empty else [],
        user_config=user_config
    )

if __name__ == "__main__":
    app.run(debug=True)