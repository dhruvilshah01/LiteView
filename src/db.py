import sqlite3


class DbClient:
    
    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)
    
    def get_tables(self):
        cursor = self.conn.cursor()
        res = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
        tables = res.fetchall()
        return list(map(lambda table: table[0],tables))

    def get_table_schema(self, table_name):
        cursor = self.conn.cursor()
        res = cursor.execute(f"PRAGMA table_info(\"{table_name}\");")
        schema = res.fetchall()
        return schema

    def get_table_data(self, table_name: str):
        cursor = self.conn.cursor()
        get_table_data_string = f"SELECT * from {table_name};"
        res = cursor.execute(get_table_data_string)
        table_data = res.fetchall()
        
        get_table_schema_string = f"PRAGMA table_info({table_name});"
        res = cursor.execute(get_table_schema_string)
        table_schema_info = res.fetchall()
        
        schema_columns = list(map(lambda column: column[1], table_schema_info))
        return [table_data, schema_columns]

    def run_query(self, query:str):
        cursor = self.conn.cursor()
        try:
            query_type = self.get_query_type(query)
            if(query_type == "other"):
                cursor.execute(query)
                return None
            else:
                res = cursor.execute(query)
                return [res.fetchall(), res.description]
        except():
            return "Error with SQL String"
    
    def get_query_type(self,query:str) -> str:
        type = query.strip().split(" ")[0].lower()

        if(type == "select"):
            return "select"
        else:
            return "other"