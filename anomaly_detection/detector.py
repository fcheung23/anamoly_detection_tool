from anomaly_detection.pipeline import load_data, compute_durations

class AnomalyDetector:
    def __init__(self, filepath):
        print("Loading data...")
        self.df = load_data(filepath)
        print("Computing durations...")
        self.pairs = compute_durations(self.df)
    
    def analyze(self, min_duration=60, silence_threshold=4, burst_window=10):
        results = {}
        
        # flag long durations
        long = self.pairs[self.pairs['duration_seconds'] > min_duration]
        results['long_durations'] = long
        
        return results