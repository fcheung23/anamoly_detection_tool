from anomaly_detection.detector import AnomalyDetector


detector = AnomalyDetector("hh103.csv")

results = detector.analyze()

print("\n--- Duration summary ---")
print(results["duration_summary"].head(10).to_string(index=False))

print("\n--- Burst spikes ---")
print(results["burst_spikes"].head(10).to_string(index=False))

print("\n--- Idle gaps ---")
print(results["idle_gaps"].head(10).to_string(index=False))