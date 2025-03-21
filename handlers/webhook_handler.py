from flask import Blueprint, jsonify, current_app, request
from pydantic import ValidationError
from models.income_message import IncomingMessage
from models.message import EntityType
from handlers.bot_sender import *
from config import Config
from datetime import datetime, time
import pytz

webhook_blueprint = Blueprint("webhook", __name__)

@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook_handler():
    try:
        data = request.json
        current_app.logger.info(f"Входящий запрос: {data}")

        message = IncomingMessage(**data)
        current_app.logger.info(f"Запрос успешно спарсен: {message}")

        if is_users_message(message=message) and is_test_chat(chat_id=message.chat_id):
            handle_test_chat(message_id=message.id)
        
        if is_users_message(message=message) and is_merge_chat(chat_id=message.chat_id):
            handle_merge_chat(message_id=message.id)

        return jsonify({"status": "success"}), 200

    except ValidationError as e:
        current_app.logger.error(f"Ошибка валидации: {str(e)}")
        return jsonify({"error": "Invalid incoming message format", "details": str(e)}), 400

    except Exception as e:
        current_app.logger.error(f"Ошибка при обработке запроса: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

def handle_test_chat(message_id):
    handle_merge_chat(message_id=message_id)

def handle_merge_chat(message_id):
    thread_id = create_thread(message_id)
    if may_deploy():
        current_app.logger.info("Мержить можно")
        send_mr_reminder(thread_id=thread_id)
    else:
        current_app.logger.info("Мержить нельзя")
        send_deploy_pic(thread_id=thread_id)

def is_users_message(message):
    isMessage = message.type == "message" and message.entity_type == EntityType.DISCUSSION
    return isMessage and message.user_id != current_app.config.get('BOT_ID')

def is_test_chat(chat_id):
    current_app.logger.info("Проверка тест чата")
    return chat_id == Config.TEST_CHAT_ID

def is_merge_chat(chat_id):
    current_app.logger.info("Проверка мерж чата")
    return chat_id == Config.MERGE_CHAT_ID

timezone = pytz.timezone("Europe/Moscow")
now = datetime.now(timezone)
def may_deploy():
    return 0 <= now.weekday() <= 3 and time(11, 0) <= now.time() < time(16, 0)  