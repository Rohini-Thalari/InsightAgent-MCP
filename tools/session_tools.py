from utils.session_manager import session_manager
from datetime import datetime 
from typing import Dict

def create_session_tool():
    """ Create a new analysis session.
    Sessions allow the AI agent to store: 
    - database connection 
    - cached datasets 
    - intermediate query results 
    Returns 
    ------- 
    dict { "status": "success", "data": { "session_id": "...", "created_at": "timestamp" } }
    """
    try:

        session_id = session_manager.create_session()

        return {
            "status": "success",
            "data": {
                "session_id": session_id,
                "created_at": datetime.now().isoformat()
            }
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
