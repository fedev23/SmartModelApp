# Nuevo archivo: session_manager.py
import uuid
import datetime
# Reutilizamos el session_store existente
from api.session_api import session_store

class SessionManager:
    @staticmethod
    async def get_current_session():
        """Obtiene el session_id directamente desde session_store."""
        if session_store:
            for session_id, data in session_store.items():
                if data.get("is_logged_in"):
                    return session_id
        return None
