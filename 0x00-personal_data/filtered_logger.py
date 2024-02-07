#!/usr/bin/env python3
""" function called filter_datum that
returns the log message obfuscated:"""

import re
import logging
from typing import List
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
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


PII_FIELDS = ('name',
              'email',
              'phone',
              'ssn',
              'password')


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""

    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(user=user, password=password,
                                         host=host, database=database_name)
    return connection


def main() -> None:
    """Main function to retrieve data from
    the database and log redacted fields."""
    logger = get_logger()

    # Obtain database connection
    connection = get_db()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = "; ".join(
                [f"{field}={value}" for field, value in zip(
                    cursor.column_names, row)])
            logger.info(formatted_row)
    except mysql.connector.Error as err:
        logger.error("Error retrieving data from database: %s", err)
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()
