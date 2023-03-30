#!/usr/bin/env python3
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cur = self.connection.cursor()

    def create_table(self):
        self.cur.execute('DROP TABLE IF EXISTS transactions')
        self.cur.execute('''CREATE TABLE transactions(
                                Client varchar, 
                                Date timestamp, 
                                Description text, 
                                Withdrawals int, 
                                Deposits int, 
                                Balance int
                            )'''
                        )
        self.connection.commit()

    def deposit(self, new_data):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = new_data.get('description')
        client = new_data.get('client')
        amount = new_data.get('amount')
        self.cur.execute("""INSERT INTO transactions 
                            VALUES( ?, ?, ?, ?, ?, ?)""", 
                            (client, date, description, 0, amount, float(amount) + self.check_balance(client))
                        )
        self.connection.commit()

    def withdraw(self, new_data):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = new_data.get('description')
        client = new_data.get('client')
        amount = new_data.get('amount')
        self.cur.execute("""INSERT INTO transactions 
                            VALUES( ?, ?, ?, ?, ?, ?)""", 
                            (client, date, description, amount , 0, self.check_balance(client) - float(amount))
                        )
        self.connection.commit()

    def check_balance(self, name):
        self.cur.execute("""SELECT Deposits, Withdrawals
                            FROM transactions 
                            WHERE Client = ?""", (name,)
                        )
        balance = 0
        for transaction in self.cur.fetchall():
            balance += transaction[0] - transaction[1]
        return balance

    def show_bank_statement(self, req):
        client = req.get('client')
        since = req.get('since')
        till = req.get('till')
        self.cur.execute("""SELECT Date, Description, Withdrawals, Deposits, Balance 
                            FROM transactions WHERE Client = ?
                            AND Date > ?
                            AND Date < ?
                            """,
                            (client, since, till)
                         )
        return self.cur.fetchall()

    def close(self):
        self.connection.close()


def main():
    db = Database(filename='db.sqlite3')
    db.close()


if __name__ == "__main__":
    main()
