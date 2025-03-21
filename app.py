from flask import Flask, current_app
from flask_apscheduler import APScheduler
import logging
from logging.handlers import TimedRotatingFileHandler
from config import Config
from handlers.webhook_handler import webhook_blueprint
from handlers.bot_sender import send_message_to_bot, send_core_standup_reminder, send_interface_standup_reminder
from datetime import datetime

# Настройка логирования
log_handler = TimedRotatingFileHandler("logs/app.log", when="D", interval=3, backupCount=1)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(), log_handler]
)

app = Flask(__name__)
app.config.from_object(Config)

# Регистрируем Blueprint для обработки вебхуков
app.register_blueprint(webhook_blueprint)

def log_reminder():
    with app.app_context():
        send_message_to_bot("Cреда — маленькая пятница, но Jira не знает об этом\nдружеское напоминание: залогать время 🕒\nвремя само себя не залогает 😉")

def standup_core_reminder():
    with app.app_context():
        send_core_standup_reminder()

def standup_interface_reminder():
    with app.app_context():
        send_interface_standup_reminder()

# Инициализируем и запускаем планировщик
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(
    id="log_reminder_job",
    func=log_reminder,
    trigger="cron",
    day_of_week="wed",
    hour=10,
    minute=00,
    replace_existing=True
)
scheduler.add_job(
    id="standup_core_reminder_job",
    func=standup_core_reminder,
    trigger="cron",
    day_of_week="mon-fri",
    hour=11,
    minute=30,
    replace_existing=True
)
scheduler.add_job(
    id="standup_interface_reminder_job",
    func=standup_interface_reminder,
    trigger="cron",
    day_of_week="mon-fri",
    hour=11,
    minute=00,
    replace_existing=True
)

if __name__ == "__main__":
    app.run(use_reloader=False)