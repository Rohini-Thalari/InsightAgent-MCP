import uuid
import time

class SessionManager:

    def __init__(self):
        self.sessions = {}

    def create_session(self):

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "db_engine": None,
            "datasets": {},
            "cache": {},
            "created_at": time.time()
        }

        return session_id

    def get_session(self, session_id):

        if session_id not in self.sessions:
            raise ValueError(f"Invalid session:{session_id}")

        return self.sessions[session_id]

    def get_engine(self, session_id):
        session = self.get_session(session_id)
        engine = session.get("db_engine")
        if engine is None:
            raise RuntimeError(f"No database connected for session: {session_id}")
        return engine

    def delete_session(self, session_id):

        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self):
        return list(self.sessions.keys())

session_manager = SessionManager()