# Testing Moodle API

# importing the module
from moodleAPI import MoodleAPI
from bs4 import BeautifulSoup

# Load configuration from config.ini
api = MoodleAPI("config.ini")

# Login to Moodle using credentials from config.ini
api.login(api.config["moodle"]["username"], api.config["moodle"]["password"])




notifications = api.get_popup_notifications(27436)
count = api.popup_notification_acknowledge(27436)

print(f"You have {count} unread notifications.")

# for notification in notifications["notifications"]:
#     data = f"""ID: {notification["id"]}
# Subject: {notification["subject"]}
# --------"""
#     print(data)

newest = notifications["notifications"][0]
# print(newest)



#Parse the text from the html
html = newest["fullmessagehtml"]
soup = BeautifulSoup(html, "html.parser")
text = soup.get_text()
# remove empty lines
text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
print(text)