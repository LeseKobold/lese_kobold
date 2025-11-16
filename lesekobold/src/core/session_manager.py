from __future__ import annotations

import logging
import uuid

import google.adk
import google.adk.sessions

logging.basicConfig(level=logging.ERROR)


class SessionManager:
    """Manager for sessions."""

    def __init__(
        self,
        session_service: google.adk.sessions.InMemorySessionService,
        app_name: str,
    ):
        self.session_service = session_service
        self.name = app_name

    async def get_or_create_session(
        self, user_id: str, session_id: str | None = None
    ) -> google.adk.sessions.Session | None:
        """Get or create a session for the user."""

        if not session_id:
            # Create a new session
            try:
                session_id = uuid.uuid4()
                new_session: google.adk.sessions.Session = (
                    self.session_service.create_session(
                        app_name=self.name,
                        user_id=user_id,
                        session_id=session_id,
                        state={},
                    )
                )
            except Exception as e:
                logging.error(
                    f"Failed to create new session for user '{user_id}' "
                    f"for app '{self.name}' due to error: {e}"
                )
                return None
            logging.info(
                f"Created session '{session_id}' "
                f"for user '{user_id}' "
                f"for app '{self.name}'."
            )

        # Get an existing session (and check that creation was successful)
        try:
            session: google.adk.sessions.Session = (
                await self.session_service.get_session(
                    app_name=self.name,
                    user_id=user_id,
                    session_id=session_id,
                )
            )
            if not session:
                raise Exception(
                    f"Session is 'None' for user '{user_id}' and session '{session_id}' and app '{self.name}'."
                )
        except Exception as e:
            logging.error(
                f"Failed to retrieve session '{session_id}' "
                f"for user '{user_id}' "
                f"for app '{self.name}' due to error: {e}"
            )
            return None
        logging.info(
            f"Retrieved session '{session.id}' "
            f"for user '{session.user_id}' "
            f"for app '{session.app_name}'."
        )
        return session

    @staticmethod
    def get_session_service(app_name: str) -> "SessionManager":
        # FIXME: add in memory session service
        return SessionManager(
            session_service=google.adk.sessions.InMemorySessionService(),
            app_name=app_name,
        )
