from anomaly_detection.detector import AnomalyDetector
from anomaly_detection.report import print_report

detector = AnomalyDetector("weekendaway_fixed.csv")
detector.configure({
    "idle_gap": {
        "threshold_seconds": 20 * 60 * 60,
        "housewide_sensor_ratio": 0.8,
        "return_window_minutes": 60,
    }
})

results = detector.analyze()
print_report(results)
