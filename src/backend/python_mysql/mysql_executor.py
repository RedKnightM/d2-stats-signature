from backend.python_mysql.mysql_connector import SQLConnector
from backend.python_mysql.mysql_commands import InsertCommand, SelectCommand
from backend.bng_python.bng_data import BungieData

class DatabaseExecutor:
    """
    Handles executing basic queries on the D2 stats database. 
    """
    def __init__(self, db: SQLConnector) -> None:
        self.__db = db
        self.__insert_command: InsertCommand = InsertCommand(db)
        self.__select_command: SelectCommand = SelectCommand(db)

    def insert_row(self, table_name: str, data: BungieData):
        """
        Insert row(s) into a table
        """
        self.__insert_command.set_command(table_name, data)
        self.__insert_command.execute()

    def select_rows(self, table_name: str, fields: list[str], condition: dict):
        """
        Retrieve rows or sepcfifc columns of a row from a table
        """
        self.__select_command.set_command(table_name, fields, condition)
        return self.__select_command.execute()

    def retrieve_all(self, table_name: str):
        return self.__db.retrieve_all(table_name)
    
def main():
    conn = SQLConnector("test", 33061)
    executor = DatabaseExecutor(conn)

    result = executor.select_rows("`Weapon`", ["weapon_id"], {"bng_weapon_id": 1916287826})
    print(result)

if __name__ == "__main__":
    main()
