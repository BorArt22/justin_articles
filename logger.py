'''
Log message to logging.INFO level using next format:
    [{time in format %d/%m/%Y, %H:%M:%S}] {code_part}: {message}

input:
    code_part - string. Part where running log_message.
    message - string. Message that will be displayed.
'''

import logging

from datetime import datetime

logging.basicConfig(level=logging.INFO)

def log_message(code_part,message):
    logging.info('[{time}] {code_part}: {message}'.format(
        time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), code_part=code_part, message=message))