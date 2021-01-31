import time
import os
from telethon import TelegramClient, events
import click
from config import LOG_CONFIG
import logging.config
logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger(__name__)

@click.command()
@click.option('--message')
def autoreply(message:str):
    api_id = os.environ['AUTOREPLY_API_ID']
    api_hash = os.environ['AUTOREPLY_API_HASH']
    phone = os.environ['AUTOREPLY_PHONE']
    password = os.environ['AUTOREPLY_PASSWORD']
    session_file = os.environ['AUTOREPLY_SESSION_FILE']




    users = [] # To send message only once for each user 
    # Create the client and connect
    # use sequential_updates=True to respond to messages one at a time
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)


    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        if event.is_private:  # only auto-reply to private chats
            from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            if not from_.bot:  # don't auto-reply to bots
                logger.debug(event.message)  # optionally log time and message
                if event.from_id not in users:
                    await event.respond(message)
                    users.append(event.from_id)


    logger.info('Auto-replying...')
    client.start(phone, password)
    client.run_until_disconnected()
    logger.info('Stopped!')



if __name__ == '__main__':
   autoreply()

    