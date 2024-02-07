#!/usr/bin/env python3
""" function called filter_datum that
returns the log message obfuscated:"""

import re
import logging
from typing import List


def filter_datum(fields: str, redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for f in fields:
        message = re.sub(rf'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR)
        return super().format(record)
