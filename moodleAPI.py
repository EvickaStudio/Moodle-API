import configparser
import requests
import logging


class MoodleAPI:
    """
    MoodleAPI

    A class that provides methods for interacting with the Moodle API.

    Attributes:
        config (ConfigParser): The configuration parser object.
        url (str): The URL of the Moodle instance.
        session (Session): The requests session object.
        requestHeader (dict): The headers for the requests.
        token (str): The authentication token.
        userid (str): The user ID.

    Methods:
        __init__(config_file: str) -> None:
            Initializes the MoodleAPI object.

        login(username: str, password: str) -> bool:
            Logs in to the Moodle instance.

        get_site_info() -> dict:
            Retrieves site information from the Moodle instance.

        get_popup_notifications(user_id: str) -> dict:
            Retrieves popup notifications for a user.

        popup_notification_acknowledge(user_id: str) -> dict:
            Acknowledges popup notifications for a user.

        _post(arg0: str, user_id: str) -> dict:
            Sends a POST request to the Moodle API.

    Example:
        ```python
        api = MoodleAPI("config.ini")
        api.login("username", "password")
        site_info = api.get_site_info()
        print(site_info)
        ```
    """

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.url = self.config["moodle"]["moodleUrl"]
        self.session = requests.Session()
        self.requestHeader = {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2; wv) AppleWebKit/537.36"
                + " (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 MoodleMobile"
            ),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.session.headers.update(self.requestHeader)
        self.token = None
        self.userid = None

    def login(self, username, password):
        """
        login(self, username: str, password: str) -> bool:
            Logs in to the Moodle instance using the provided username and password.
            Sets the token for the MoodleAPI object.
        """
        login_data = {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app",
        }
        response = self.session.post(f"{self.url}login/token.php", data=login_data)
        if "token" in response.text and "privatetoken" in response.text:
            logging.info("Login successful")
            self.token = response.json()["token"]
            return True
        else:
            logging.error("Login failed")
            return False

    def get_site_info(self):
        """
        get_site_info(self) -> dict:
            Retrieves site information from the Moodle instance.
        """
        if self.token is None:
            logging.error("Token not set. Please login first.")
            return None
        wsfunction = "core_webservice_get_site_info"
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "moodlewsrestformat": "json",
        }
        response = self.session.post(
            f"{self.url}webservice/rest/server.php", params=params
        )
        self.userid = response.json()["userid"]
        return response.json()

    def get_popup_notifications(self, user_id):
        """
        Retrieves popup notifications for a user.
        """
        return self._post("message_popup_get_popup_notifications", user_id)

    def popup_notification_unread_count(self, user_id):
        """
        Retrieves the number of unread popup notifications for a user.
        """
        return self._post("message_popup_get_unread_popup_notification_count", user_id)

    def _post(self, arg0, user_id):
        """
        Sends a POST request to the Moodle API with an given wsfunction and user ID.
        """
        if self.token is None:
            logging.error("Token not set. Please login first.")
            return None
        wsfunction = arg0
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "useridto": user_id,
            "moodlewsrestformat": "json",
        }
        response = self.session.post(
            f"{self.url}webservice/rest/server.php", params=params
        )
        return response.json()
