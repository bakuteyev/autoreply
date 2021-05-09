

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import logging
import os


import yandexcloud
import json

from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.compute.v1.instance_service_pb2 import (
    ListInstancesRequest, StartInstanceRequest, StopInstanceRequest,
    GetInstanceRequest
    )
from yandex.cloud.compute.v1.instance_pb2 import Instance
from time import sleep
from io import StringIO
import paramiko


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
telegram_token = os.environ['TELEGRAM_TOKEN']
telegram_id = int(os.environ['TELEGRAM_USER_ID'])
instance_id = os.environ['CLOUD_INSTANNCE_ID']
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher


instance_service = yandexcloud.SDK().client(InstanceServiceStub)

def _telegram_send_json(chat_id, message):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': chat_id,
            'text':  message
        }),
        'isBase64Encoded': False
    }

def autoreply(event, context, message):
    body = json.loads(event['body'])


    try:
        logger.info('Starting instance')
        instance_start = instance_service.Start(StartInstanceRequest(instance_id=instance_id))
    except:
        pass
   

    status = Instance.Status.STOPPED
    while status != Instance.Status.RUNNING:
        instance_info = instance_service.Get(GetInstanceRequest(instance_id=instance_id))
        status = instance_info.status
        sleep(5)

    ip = instance_info.network_interfaces[0].primary_v4_address.one_to_one_nat.address


    not_started = True
    keyfile = StringIO(os.environ['SSH_KEY'])
    mykey = paramiko.RSAKey.from_private_key(keyfile)
    command = f'source ~/venv/bin/activate && cd autoreply && export `cat .env` && nohup python autoreply.py --message "{message}" >/dev/null 2>&1 &'
    ssh = paramiko.SSHClient()

    while not_started:
        sleep(1)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username='bakuteev', pkey=mykey)
        transport = ssh.get_transport()
        channel = transport.open_session()
    
        channel.exec_command(command)
        not_started = False
    return _telegram_send_json(body['message']['chat']['id'],  f'Will autoreply: {message}')


def stopautoreply(event, context, message):
    body = json.loads(event['body'])
    try:
        logger.info('Stopping instance')
        instance_stop = instance_service.Stop(StopInstanceRequest(instance_id=instance_id))
    except:
        pass

    return _telegram_send_json(body['message']['chat']['id'],  instance_stop)

def send_message(event, context):
    body = json.loads(event['body'])
  
    message = body['message']['text']

    if (int(body['message']['chat']['id']) == telegram_id):
        if message.startswith('/autoreply '):
            reply_message =  message[len('/autoreply '):]
            return autoreply(event, context, reply_message)

        if (message == '/stopautoreply'):
            return stopautoreply(event, context, None)

