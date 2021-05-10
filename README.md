# Autoreply
At the moment this is auto replier for telegram only.
Inspired by https://medium.com/@jiayu./automatic-replies-for-telegram-85075f28321

The main diffrence is that this script is running in Yandex Cloud and 
is triggerred by telegram bot via cloud function.


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

The main file is `autoreply.py`. Files related to triger are located in `cloud_function` folder.

More info is here https://bakuteev.website.yandexcloud.net/posts/blog-telegram-autoreply-yandex-cloud
