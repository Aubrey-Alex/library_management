from utils.db_connector import DBConnector

# 查询总藏书量
def total_books_query():
    db = DBConnector()
    db.connect()
    query = "SELECT SUM(total_nums) AS total_books FROM books"
    result = db.execute_query(query)
    db.close()
    if result[0][0] is None:
        return 0
    return result[0][0]

# 查询已借出的书籍数量
def borrowed_books_query():
    db = DBConnector()
    db.connect()
    query = "SELECT COUNT(*) AS borrowed_books FROM borrow_records WHERE return_date IS NULL"
    result = db.execute_query(query)
    db.close()
    if result[0][0] is None:
        return 0
    return result[0][0]

# 查询累计借阅书籍数量
def accumulated_borrowed_books_query():
    db = DBConnector()
    db.connect()
    query = "SELECT COUNT(*) AS accumulated_borrowed_books FROM borrow_records"
    result = db.execute_query(query)
    db.close()
    if result[0][0] is None:
        return 0
    return result[0][0]

if __name__ == '__main__':
    print(total_books_query())
    print(borrowed_books_query())
    print(accumulated_borrowed_books_query())