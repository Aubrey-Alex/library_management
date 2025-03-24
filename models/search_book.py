from utils.db_connector import DBConnector

def build_query(conditions, sort_by="title", order_by="asc"):
    """
    构建 SQL 查询语句
    :param conditions: 查询条件字典，键为字段名，值为条件值
    :param sort_by: 排序字段，默认为书名（title）
    :param order_by: 排序方式，默认为递增（asc）
    :return: 构建的 SQL 查询语句和参数列表
    """
    base_query = "SELECT book_id, category, title, press, year, author, price, total_nums, stock FROM books"
    where_clauses = []
    params = []

    # 处理查询条件
    if conditions.get("category"):
        where_clauses.append("category = ?")
        params.append(conditions["category"])
    if conditions.get("title"):
        where_clauses.append("title LIKE ?")
        params.append(f"%{conditions['title']}%")
    if conditions.get("press"):
        where_clauses.append("press = ?")
        params.append(conditions["press"])
    if conditions.get("year_start"):
        where_clauses.append("year >= ?")
        params.append(conditions["year_start"])
    if conditions.get("year_end"):
        where_clauses.append("year <= ?")
        params.append(conditions["year_end"])
    if conditions.get("author"):
        where_clauses.append("author LIKE ?")
        params.append(f"%{conditions['author']}%")
    if conditions.get("price_min"):
        where_clauses.append("price >= ?")
        params.append(conditions["price_min"])
    if conditions.get("price_max"):
        where_clauses.append("price <= ?")
        params.append(conditions["price_max"])

    # 组合 WHERE 子句
    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)

    # 添加排序
    base_query += f" ORDER BY {sort_by} {order_by}"

    # 限制返回结果数量
    base_query += " LIMIT 50"

    return base_query, params

def search_books(conditions, sort_by="title", order_by="asc"):
    """
    查询图书信息
    :param conditions: 查询条件字典
    :param sort_by: 排序字段，默认为书名（title）
    :param order_by: 排序方式，默认为递增（asc）
    :return: 符合条件的图书列表
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    # 构建查询语句
    query, params = build_query(conditions, sort_by, order_by)
    
    # 执行查询
    result = db.execute_query(query, params)
    
    # 关闭数据库连接
    db.close()
    
    # 返回json格式
    books =[]
    for row in result:
        book = {
            "book_id": row[0],
            "category": row[1],
            "title": row[2],
            "press": row[3],
            "year": row[4],
            "author": row[5],
            "price": row[6],
            "total_nums": row[7],
            "stock": row[8]
        }
        books.append(book)

    return books

def default_books():
    """
    默认图书信息
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    # 构建查询语句
    query = "SELECT book_id, category, title, press, year, author, price, total_nums, stock FROM books LIMIT 10"
    # 执行查询
    result = db.execute_query(query)
    
    # 关闭数据库连接
    db.close()
    
    # 返回json格式
    books =[]
    for row in result:
        book = {
            "book_id": row[0],
            "category": row[1],
            "title": row[2],
            "press": row[3],
            "year": row[4],
            "author": row[5],
            "price": row[6],
            "total_nums": row[7],
            "stock": row[8]
        }
        books.append(book)

    return books

def query_books(conditions, order_by="title"):
    """
    查询图书信息
    :param conditions: 查询条件字典
    :param order_by: 排序字段，默认为书名（title）
    :return: 符合条件的图书列表
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    # 构建查询语句
    query, params = build_query(conditions, order_by)

    print("条件：", conditions)
    print("排序：", order_by)
    print("查询语句：", query)
    print("参数：", params)

    # 执行查询
    result = db.execute_query(query, params)
    
    # 关闭数据库连接
    db.close()

    return result

def test_query_books():
    """
    测试图书查询功能
    """
    # 测试查询条件
    conditions = {
        "price_min": 50.00,              # 按价格区间查询
        "price_max": 100.00
    }

    # 调用查询函数
    books = query_books(conditions, order_by="year")  # 按年份排序

    # 输出查询结果
    if books:
        print("查询结果：")
        for book in books:
            print(book)
    else:
        print("未找到符合条件的图书。")

if __name__ == "__main__":
    # 运行测试
    test_query_books()