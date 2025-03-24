from utils.db_connector import DBConnector

def administrator_login(admin_id, password):
    """
    管理员登录功能
    :param admin_id: 管理员ID
    :param password: 密码
    :return: 登录成功返回 True，失败返回 False
    """

    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    # SQL 查询语句
    query = "SELECT * FROM administrators WHERE admin_id = ? AND password = ?"
    
    # 执行查询
    result = db.execute_query(query, (admin_id, password))
    
    # 关闭数据库连接
    db.close()

    # 检查查询结果
    if result:
        return True
    else:
        return False
 
def test_admin_login():
    """
    测试管理员登录功能
    """

    admin_id = 1
    password = '123456'

    # 调用登录函数
    if administrator_login():
        print("登录成功！")
    else:
        print("登录失败，请检查管理员ID和密码。")

if __name__ == "__main__":
    # 运行测试
    test_admin_login()