# Autoreply
At the moment this is auto replier for telegram only.
Inspired by https://medium.com/@jiayu./automatic-replies-for-telegram-85075f28321

The main diffrence is that this script will be run in
cloud and will be triggerred by cloud function. Full decription will be later.


Use to install requirements
```
pip install -r requirements.txt
```

Initialize following environment variables

```
AUTOREPLY_API_ID=...
AUTOREPLY_API_HASH=...
AUTOREPLY_PHONE=...
AUTOREPLY_SESSION_FILE=...  
AUTOREPLY_PASSWORD=...
```

To get API_ID and API_HASH follow https://core.telegram.org/api/obtaining_api_id

Use your username as SESSION_FILE by default.