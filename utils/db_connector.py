import pyodbc

class DBConnector:
    """
    数据库连接器类
    """

    # 初始化连接器
    def __init__(self):
        self.conn_str = 'DSN=MySQL8.0_library_management;SERVER=localhost;DATABASE=library_management;UID=root;PWD=060122;'
        self.conn = None
        self.cursor = None

    # 连接数据库
    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            print("Database connected successfully！")
        except Exception as e:
            print("Database connection failed：", e)

    # 关闭数据库连接
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed。")

    # 执行插入语句
    def execute_insert(self, insert, params=None):
        try:
            if params:
                self.cursor.execute(insert, params)
            else:
                self.cursor.execute(insert)
            self.conn.commit()
            print("Insert operation successful！")
        except Exception as e:
            print("Insert operation failed：", e)

    # 执行删除语句
    def execute_delete(self, delete, params=None):
        try:
            if params:
                self.cursor.execute(delete, params)
            else:
                self.cursor.execute(delete)
            self.conn.commit()
            print("Delete operation successful！")
        except Exception as e:
            print("Delete operation failed：", e)

    # 执行更新语句
    def execute_update(self, update, params=None):
        try:
            if params:
                self.cursor.execute(update, params)
            else:
                self.cursor.execute(update)
            self.conn.commit()
            print("Update operation successful！")
        except Exception as e:
            print("Update operation failed：", e)

    # 执行查询语句
    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print("Query execution failed：", e)
            return None