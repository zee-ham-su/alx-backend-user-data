#!/usr/bin/env python3
""" function called filter_datum that
returns the log message obfuscated:"""

import re


def filter_datum(fields: str, redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for f in fields:
        message = re.sub(rf'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
