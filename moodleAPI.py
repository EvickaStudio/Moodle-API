import configparser
import requests
import logging


class MoodleAPI:
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
        return self._post("message_popup_get_popup_notifications", user_id)

    def popup_notification_acknowledge(self, user_id):
        return self._post("message_popup_get_unread_popup_notification_count", user_id)

    def _post(self, arg0, user_id):
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


