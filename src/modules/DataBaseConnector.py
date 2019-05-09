import odbc


class DataBaseConnector:

    def __init__(self):
        connect = odbc.odbc('oasis')
        db = connect.cursor()
        self.db = db

    def db_reconnect(self):
        connect = odbc.odbc('oasis')
        db = connect.cursor()
        self.db = db

    def test(self):
        print("test")