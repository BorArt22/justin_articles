import logging

from datetime import datetime

logging.basicConfig(level=logging.INFO)

logging.info(f"New data was loading. Everyday scheduler work correctly.")

def log_message(code_part,message):
    logging.info('[{time}] {code_part}: {message}'.format(
        time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), code_part=code_part, message=message))