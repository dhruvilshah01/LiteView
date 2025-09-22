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
            is_select = self.is_select(query)
            if(not is_select):
                cursor.execute(query)
                return None
            else:
                res = cursor.execute(query)
                return [res.fetchall(), res.description]
        except Exception as e:
            return e
    
    def is_select(self,query:str) -> bool:
        type = query.strip().split(" ")[0].lower()
        print("TYPE IS: ", type)
        if(type.strip() == "select"):
            return "select"
        else:
            return "other"
    
    def explain_query(self,query: str):
        cursor = self.conn.cursor()
        try:
            res = cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            return res.fetchall()
        except Exception as e:
            return e