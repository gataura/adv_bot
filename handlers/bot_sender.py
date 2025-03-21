import requests
from flask import current_app
from models.message import MessageWrapper, Message, EntityType, File
from config import Config
import json

def send_request_to_bot(data):
    current_app.logger.info(f"Запрос: {data}")
    try:
        response = requests.post(
            current_app.config.get('BOT_ENDPOINT'),
            json=data,
            timeout=5
        )

        if response.ok:
            current_app.logger.info(f"Сообщение отправлено: {response.json()}")
        else:
            current_app.logger.error(f"Ошибка отправки реквеста {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Не удалось подключиться к боту: {e}")

def send_message_to_bot(message):
    data = {"message": message}

    send_request_to_bot(data)

def send_deploy_pic(thread_id):
    current_app.logger.info("Отправка картинки")
    text = standup_text = "ATTENTION PLEASE!!"

    file = File(
        key = Config.DEPLOY_PIC_URL,
        name = "deploy_adv.jpeg",
        file_type = "image",
        size = 68370,
        width = 1000,
        height = 562
    )
    files = [file]
    messageInterface = Message(
        entity_type = EntityType.THREAD,
        entity_id = thread_id,
        content = text,
        link_preview = False,
        files = files
    )
    send_message(message=messageInterface)

def send_mr_reminder(thread_id):
    message = Message(
        entity_type = EntityType.THREAD,
        entity_id = thread_id,
        content = "В этом проекте мы не просто мержим…\nМы мержим с чеклистом.\nПотому что у нас есть семья и ответственность перед ревьюерами 🛠️"
    )
    send_message(message=message)

def send_core_standup_reminder():
    current_app.logger.info("Отправка напоминания о стендапе коры")
    text = standup_text = "🚀 Друзья, пора на стендап!\nПодключайтесь: https://meet.pachca.com/adv-core-07d63791"

    core_chat_id = Config.CORE_CHAT_ID
    messageCore = Message(
        entity_type = EntityType.DISCUSSION,
        entity_id = core_chat_id,
        content = text,
        link_preview = False
    )
    send_message(message=messageCore)

def send_interface_standup_reminder():
    current_app.logger.info("Отправка напоминания о стендапе интерфейса")
    text = standup_text = "🚀 Друзья, пора на стендап!\nПодключайтесь: https://meet.pachca.com/adv-interface-8db1807d"

    interface_chat_id = Config.INTERFACE_CHAT_ID
    messageInterface = Message(
        entity_type = EntityType.DISCUSSION,
        entity_id = interface_chat_id,
        content = text,
        link_preview = False
    )
    send_message(message=messageInterface)


def create_thread(message_id):
    url = f"https://api.pachca.com/api/shared/v1//messages/{message_id}/thread"
    headers = {Config.API_TOKEN}
    
    try:
        response = requests.post(url, headers=headers, timeout=5)
        
        if response.ok:
            thread_id = response.json().get("data").get("id")
            current_app.logger.info(f"Тред создан: {thread_id}")
            return thread_id
        else:
            current_app.logger.error(f"Ошибка создания треда {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Не удалось создать тред: {e}")
    
    return None
    
def send_message_to_thread(message, thread_id):
    data = {"message": message, "thread_id": thread_id}
    send_request_to_bot(data)

def send_message(message):
    request = MessageWrapper(message=message)
    headers = Config.HEADERS
    json = request.model_dump()
    current_app.logger.info(f"Запрос: {json}")
    try:
        response = requests.post(
            current_app.config.get('MESSAGE_ENDPOINT'),
            headers=headers,
            json=json,
            timeout=5
        )

        if response.ok:
            current_app.logger.info(f"Сообщение отправлено: {response.json()}")
        else:
            current_app.logger.error(f"Ошибка отправки реквеста {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Не удалось подключиться к боту: {e}")