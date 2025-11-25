"""Session & long-term memory utility."""
import threading, json, os
_PERSIST_PATH = "project/memory/long_term_memory.json"
class SessionMemory:
    def __init__(self):
        self._lock = threading.Lock()
        self._sessions = {}
        self._long_term = self._load() or {}

    def _load(self):
        try:
            if os.path.exists(_PERSIST_PATH):
                with open(_PERSIST_PATH, "r") as f:
                    return json.load(f)
        except Exception:
            return {}
        return {}

    def _save(self):
        try:
            with open(_PERSIST_PATH, "w") as f:
                json.dump(self._long_term, f)
        except Exception:
            pass

    def get_session(self, sid):
        with self._lock:
            return self._sessions.setdefault(sid, {})

    def set_session_value(self, sid, key, value):
        with self._lock:
            sess = self._sessions.setdefault(sid, {})
            sess[key] = value

    def get_long_term(self, key, default=None):
        return self._long_term.get(key, default)

    def set_long_term(self, key, value):
        self._long_term[key] = value
        self._save()

default_memory = SessionMemory()
