from utils.db_connector import DBConnector

def insert_borrower(name, workplace, type):
    """
    新增借书证
    :param name: 借书人姓名
    :param workplace: 工作单位
    :param type: 身份类别
    """

    # 初始化数据库连接器
    db = DBConnector()
    db.connect()
    try:
        # 查询是否已经有该借书证
        query = "SELECT * FROM borrowers WHERE name = ? AND workplace = ? AND type = ?"
        params = (name, workplace, type)
        result = db.execute_query(query, params)
        if len(result) > 0:
            return
        # 如果没有该借书证，则插入新借书证
        max_card_id_query = "SELECT MAX(card_id) FROM borrowers"
        result = db.execute_query(max_card_id_query)
        if len(result) > 0 and result[0][0] is not None:
            card_id = result[0][0] + 1
        else:
            card_id = 1
        # SQL 插入语句
        insert = "INSERT INTO borrowers (card_id, name, workplace, type) VALUES (?,?,?,?)"
        print("新增借书证：", insert, (card_id, name, workplace, type))
        # 执行插入
        db.execute_insert(insert, (card_id, name, workplace, type))
    except Exception as e:
        print("新增借书证失败:", e)
        return False
    finally:
        # 关闭数据库连接
        db.close()

    return True

def delete_borrower(card_id, name):
    """
    删除借书证
    :param card_id: 借书证卡号
    """

    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    try:
        # 查询是否有该借书证
        query = "SELECT * FROM borrowers WHERE card_id = ? AND name = ?"
        params = (card_id, name)
        result = db.execute_query(query, params)
        if len(result) == 0:
            return

        # SQL 删除语句
        delete = "DELETE FROM borrowers WHERE card_id = ?"

        # 执行删除
        db.execute_delete(delete, (card_id,))
    except Exception as e:
        print("删除借书证失败:", e)
        return False
    finally:
        # 关闭数据库连接
        db.close()

def search_borrowers(name):
    """
    搜索借书证
    :param name: 借书人姓名
    :return: 借书证列表
    """

    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    try:
        # SQL 查询语句
        query = "SELECT * FROM borrowers WHERE name LIKE ?"
        params = ('%' + name + '%',)
        result = db.execute_query(query, params)
        borrowers = []
        for row in result:
            borrower = {
                'card_id': row[0],
                'name': row[1],
                'workplace': row[2],
                'type': row[3]
            }
            borrowers.append(borrower)
    except Exception as e:
        print("搜索借书证失败:", e)
        return []
    finally:
        # 关闭数据库连接
        db.close()

    return borrowers

def default_borrowers():
    """
    默认借书证
    """

    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    try:
        # SQl查询语句
        query = "SELECT * FROM borrowers LIMIT 3"
        result = db.execute_query(query)
        borrowers = []
        for row in result:
            borrower = {
                'card_id': row[0],
                'name': row[1],
                'workplace': row[2],
                'type': row[3]
            }
            borrowers.append(borrower)
        return borrowers
    except Exception as e:
        print("默认借书证查询:", e)
        return []
    finally:
        # 关闭数据库连接
        db.close()

def test_borrowers_admin():
    """
    测试借书证管理功能
    """

    # 新增借书证
    insert_borrower("1", "借书人1", "工作单位1", "学生")
    insert_borrower("2", "借书人2", "工作单位2", "教师")
    
if __name__ == "__main__":
    # 运行测试
    test_borrowers_admin()

    

