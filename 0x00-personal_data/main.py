#!/usr/bin/env python3
"""
Main file
"""

import mysql.connector  # Import the MySQL connector module

# Import the get_db function from filtered_logger module
from filtered_logger import get_db

try:
    # Attempt to establish a database connection
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()
except mysql.connector.Error as err:
    # Handle any errors that occur during the database connection process
    print("Error connecting to the database:", err)
