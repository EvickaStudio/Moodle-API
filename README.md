# Moodle API Wrapper for Python

- Tested and build for the [THL Lernraum](https://lernraum.th-luebeck.de/)

## Abstract

This project aims to develop a simple and easy-to-use Python API wrapper for Moodle.The wrapper will handle authentication, session management, and basic data retrieval. This wrapper is a standalone project, i intended to create a separate project that will deploy it as a notification bot with potential AI integrations like GPT-3/GPT-4 for summarizing or classifying the data.

## Features

### Core
- **Authentication**: Handle login and maintain session.
- **Data Retrieval**: Methods for fetching site info and notifications.

## Implementation Details

### Methods
- `login(username, password)`: Authenticate and initialize session.
- `get_site_info()`: Retrieve site-specific information.
- `get_popup_notifications(user_id)`: Fetch user-specific popup notifications.
- `popup_notification_unread_count(user_id)`: Fetch user-specific unread popup notifications count.

## To-Do List
1. Complete current methods.
2. Extend wrapper with additional Moodle API endpoints.

## Usage

Example of initializing and using the wrapper:

```python
moodle = MoodleAPI()
if moodle.login("username", "password"):
    site_info = moodle.get_site_info()
    print(site_info)
    notifications = moodle.get_popup_notifications(site_info["userid"])
    print(notifications) # Print all notifications
    print(notifications["notifications"][0]) # Prints the latest notification
```

## Additional Remarks
- Wrapper is independent and intended for use in a separate server-deployed application.
- Token-based authentication and session management is implemented.
  
## Contributing
- Contributions for extending functionality are welcome.

## Inspiration

- moodle-dl

## Roadmap
- Improve while studying
- Rewrite in another programming language like java or go
- Deploy on server -> get data to your phone

## Caveats and Observations

- Moodle's official API documentation lacks comprehensiveness; code inspection from alternative projects is often required for better understanding for non professional developers.
- Deviation from standard REST practices: API parameters are passed via URL, not in the request body.
- Accurate wsfunction (Web Service Functions) and its corresponding parameters are prerequisites for specific data retrieval. Many of these functions wont work due to the lack of permissions or implementation on the server side.
- API's base URL structure: `subdomain.example.com/webservice/rest/server.php`.