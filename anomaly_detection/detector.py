import pandas as pd
from anomaly_detection.pipeline import load_data, compute_sessions


def format_duration(seconds: float) -> str:
    seconds = int(seconds)

    days = seconds // 86400
    seconds %= 86400

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60
    seconds %= 60

    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


DEFAULT_CONFIG = {
    "duration_bounds": {
        "default": {"min": 5, "max": 4 * 60 * 60},
        "Bathroom": {"min": 30, "max": 60 * 60},
        "Bedroom": {"min": 60, "max": 12 * 60 * 60},
    },

    "burst": {
        "window": "1h",
        "min_sessions": 6
    },

    "idle_gap": {
        "threshold_seconds": 24 * 60 * 60
    }
}


class AnomalyDetector:
    def __init__(self, filepath, config=None):
        print("Loading data...")
        self.df = load_data(filepath)
        print("✔ Data loaded")

        print("Computing sessions...")
        self.sessions = compute_sessions(self.df)
        print("✔ Sessions computed")

        self.config = {**DEFAULT_CONFIG, **(config or {})}

    # ----------------------------
    # 1. Duration behavior summary
    # ----------------------------
    def analyze_duration(self):
        cfg = self.config["duration_bounds"]
        results = []

        print("Running duration analysis...")

        for sensor, group in self.sessions.groupby("sensor"):
            rules = cfg.get(sensor, cfg["default"])

            short = (group["duration_seconds"] < rules["min"]).sum()
            long = (group["duration_seconds"] > rules["max"]).sum()

            results.append({
                "sensor": sensor,
                "short_sessions": int(short),
                "long_sessions": int(long)
            })

        print("✔ Duration analysis complete")
        return pd.DataFrame(results)

    # ----------------------------
    # 2. Burst detection (session rate spikes)
    # ----------------------------
    def analyze_burst(self):
        cfg = self.config["burst"]
        results = []

        print("Running burst analysis...")

        for sensor, group in self.sessions.groupby("sensor"):
            group = group.sort_values("start")

            hourly_counts = group.set_index("start").resample(cfg["window"]).size()

            spikes = hourly_counts[hourly_counts >= cfg["min_sessions"]]

            for time, count in spikes.items():
                results.append({
                    "sensor": sensor,
                    "time_window": time,
                    "session_count": int(count)
                })

        print("✔ Burst analysis complete")
        return pd.DataFrame(results)

    # ----------------------------
    # 3. Idle gap detection (with days support)
    # ----------------------------
    def analyze_idle_gaps(self):
        cfg = self.config["idle_gap"]
        results = []

        print("Running idle gap analysis...")

        for sensor, group in self.sessions.groupby("sensor"):
            group = group.sort_values("start")

            gaps = group["start"].diff().dt.total_seconds()

            long_gaps = gaps[gaps > cfg["threshold_seconds"]]

            for idx, gap in long_gaps.items():
                results.append({
                    "sensor": sensor,
                    "start": group.loc[idx, "start"],
                    "idle_time": format_duration(gap)
                })

        print("✔ Idle gap analysis complete")
        return pd.DataFrame(results)

    # ----------------------------
    # Master analyze
    # ----------------------------
    def analyze(self):
        print("\n=== Starting anomaly analysis ===")

        results = {
            "duration_summary": self.analyze_duration(),
            "burst_spikes": self.analyze_burst(),
            "idle_gaps": self.analyze_idle_gaps()
        }

        print("✔ All analysis complete\n")
        return results