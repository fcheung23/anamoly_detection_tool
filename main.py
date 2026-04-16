from anomaly_detection.detector import AnomalyDetector

detector = AnomalyDetector("hh103.csv") # create detector object
results = detector.analyze(min_duration=60)         
print(results['long_durations'])        