import sqlite3
import sqlite3.dbapi2 as DBAPI2
from pathlib import Path
from typing import Dict
from cryptography.fernet import Fernet


class AccountDB:
    def __init__(self, DB: Path, key: bytes | None, keyFile: Path | None = None):
        if not DB.exists():
            DB.touch()
            self.DB = DB
        if keyFile and keyFile.exists():
            self.keyFile = keyFile
            with keyFile.open("rb") as f:
                key = f.read()
        self.DB = DB
        self.key = key
        with DBAPI2.connect(DB) as DB_Conn:
            DB_Cursor = DB_Conn.cursor()
            DB_Cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Accounts'")
            table_exists = bool(DB_Cursor.fetchone())
            if not table_exists:
                DB_Cursor.execute(
                    """CREATE TABLE Accounts
                    (username text, password text)""")

    def _encrypt(self, data: bytes) -> bytes:
        cipher = Fernet(self.key)
        return cipher.encrypt(data)

    def _decrypt(self, data: bytes) -> bytes:
        cipher = Fernet(self.key)
        return cipher.decrypt(data)

    def get_accounts(self):
        with DBAPI2.connect(self.DB) as DB_Conn:
            DB_Cursor = DB_Conn.cursor()
            DB_Cursor.execute("SELECT * FROM Accounts")
            rows = DB_Cursor.fetchall()
            decrypted_rows = [(self._decrypt(row[0]), self._decrypt(row[1])) for row in rows]
            return decrypted_rows

    def add_accounts(self, accounts: list[Dict[str, str]]):
        with DBAPI2.connect(self.DB) as DB_Conn:
            DB_Cursor = DB_Conn.cursor()
            for index, account in enumerate(accounts):
                if not account["password"]:
                    raise ValueError(f"{account} at index {index} doesn't contain a password value")
                if not account["username"]:
                    raise ValueError(f"{account} at index {index} doesn't contain a username value")
                print(f"Adding {account['username']}")

                # Check if username already exists
                DB_Cursor.execute("SELECT COUNT(*) FROM Accounts WHERE username = ?",
                                  (self._encrypt(account["username"].encode()),))
                count = DB_Cursor.fetchone()[0]
                if count > 0:
                    print(f"Skipping {account['username']}, already exists")
                    continue

                # Insert account into Accounts table
                DB_Cursor.execute("INSERT INTO Accounts (username, password) VALUES (?, ?)",
                                  (self._encrypt(account["username"].encode()),
                                   self._encrypt(account["password"].encode())))
            DB_Conn.commit()

    def remove_duplicate_accounts(self):
        with DBAPI2.connect(self.DB) as DB_Conn:
            DB_Cursor = DB_Conn.cursor()
            # Get all unique usernames
            DB_Cursor.execute("SELECT DISTINCT username FROM Accounts")
            unique_usernames = [self._decrypt(row[0]).decode() for row in DB_Cursor.fetchall()]
            # Delete all duplicate accounts
            for username in unique_usernames:
                DB_Cursor.execute("SELECT COUNT(*) FROM Accounts WHERE username = ?",
                                  (self._encrypt(username.encode())))
                account_count = DB_Cursor.fetchone()[0]
                if account_count > 1:
                    DB_Cursor.execute("DELETE FROM Accounts WHERE username = ? AND rowid NOT IN (SELECT MIN(rowid) "
                                      "FROM Accounts WHERE username = ?)", (self._encrypt(username.encode()),
                                                                            self._encrypt(username.encode())))
            DB_Conn.commit()

    def wipe_database(self) -> int:
        if not self.DB or not self.DB.exists():
            return -1
        with DBAPI2.connect(self.DB) as DB_Conn:
            DB_Cursor: sqlite3.Cursor = DB_Conn.cursor()
            DB_Cursor.execute("DELETE FROM Accounts")
            DB_Conn.commit()
            self.DB.unlink()
            if self.keyFile.exists():
                self.keyFile.unlink()
            print("Wiped!")
            return 0


class AccountManager:
    def __init__(self, AccDB: AccountDB):
        self.AccDB = AccDB

    def get_accounts(self):
        return self.AccDB.get_accounts()

    def add_accounts(self, accounts: list[Dict[str, str]]):
        return self.AccDB.add_accounts(accounts)

    def remove_duplicate_accounts(self):
        return self.AccDB.remove_duplicate_accounts()

    def wipe_database(self):
        return self.AccDB.wipe_database()
