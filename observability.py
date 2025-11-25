import json, time
LOGFILE = "project/logs.jsonl"
class Logger:
    @staticmethod
    def log(event: dict):
        entry = {"ts": time.time(), **event}
        try:
            with open(LOGFILE, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
        print("[LOG]", entry)
