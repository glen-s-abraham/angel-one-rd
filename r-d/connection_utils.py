import os
import pyotp
from logzero import logger
from dotenv import load_dotenv
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from historic_utility import HistoricUtility

# Load environment variables
load_dotenv()


class ConnectionUtility:
    """
    A utility class to manage connections with SmartApi.
    """

    def __init__(self):
        self.__api_key = os.getenv("SMART_API_KEY")
        self.__username = os.getenv("ANGEL_ONE_CLIENT_ID")
        self.__password = os.getenv("ANGEL_ONE_PIN")
        self.__totp_secret = os.getenv("ANGEL_ONE_TOTP_QR")
        self.__client = None
        self.__ws_client = None

        self._validate_env_variables()

    def _validate_env_variables(self):
        """
        Validates the required environment variables.
        Raises an exception if any are missing.
        """
        if not all(
            [self.__api_key, self.__username, self.__password, self.__totp_secret]
        ):
            logger.error(
                "Missing one or more required environment variables: SMART_API_KEY, ANGEL_ONE_CLIENT_ID, ANGEL_ONE_PIN, ANGEL_ONE_TOTP_QR"
            )
            raise ValueError("Required environment variables are not set.")

    def _generate_totp(self):
        """
        Generates a TOTP using the provided secret.
        """
        try:
            return pyotp.TOTP(self.__totp_secret).now()
        except Exception as e:
            logger.error("Failed to generate TOTP. Check your TOTP secret.")
            raise ValueError("Invalid TOTP Secret") from e

    def _start_session(self):
        """
        Initiates a session with SmartApi.
        """
        if self.__client:
            logger.info("Session already started.")
            return

        smart_api = SmartConnect(api_key=self.__api_key)
        totp = self._generate_totp()

        try:
            session_data = smart_api.generateSession(
                self.__username, self.__password, totp
            )
            if not session_data.get("status", False):
                logger.error(f"Failed to generate session: {session_data}")
                raise Exception("Error generating session.")

            self.__client = smart_api
            logger.info("Session successfully started.")
        except Exception as e:
            logger.error("Error starting session with SmartApi.")
            raise e

    def _start_ws_session(self):
        """
        Initiates a WebSocket session with SmartApi.
        """
        if self.__ws_client:
            logger.info("WebSocket session already started.")
            return

        smart_connect = self.get_client_session()
        try:
            self.__ws_client = SmartWebSocketV2(
                auth_token=smart_connect.access_token,
                api_key=self.__api_key,
                client_code=self.__username,
                feed_token=smart_connect.feed_token,
            )
            logger.info("WebSocket session successfully started.")
        except Exception as e:
            logger.error("Error starting WebSocket session.")
            raise e

    def get_client_session(self):
        """
        Retrieves the current SmartApi client session.
        Starts a new session if none exists.
        """
        if not self.__client:
            logger.info("No active session found. Starting a new session.")
            self._start_session()
        return self.__client

    def get_ws_client_session(self):
        """
        Retrieves the current SmartApi WebSocket client session.
        Starts a new session if none exists.
        """
        if not self.__ws_client:
            logger.info("No active WebSocket session found. Starting a new WebSocket session.")
            self._start_ws_session()
        return self.__ws_client
