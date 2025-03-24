from utils.db_connector import DBConnector
from datetime import datetime

def get_borrowed_books(card_id, sort_by='title', order_by='asc'):
    """
    获取某借书证所有已借书籍
    :param card_id: 借书证卡号
    :param sort_by: 排序字段
    :param order_by: 排序顺序
    :return: 已借书籍列表
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    valid_sort_by = ['book_id', 'title', 'author', 'press', 'year', 'price', 'total_nums','stock']
    valid_order_by = ['asc', 'desc']
    if sort_by not in valid_sort_by:
        sort_by = 'title'
    if order_by not in valid_order_by:
        order_by = 'asc'

    # SQL 查询语句
    query = """
    SELECT b.book_id, b.category, b.title, b.press, b.year, b.author, b.price, b.total_nums, b.stock
    FROM borrow_records br
    JOIN books b ON br.book_id = b.book_id
    WHERE br.card_id = ? AND br.return_date IS NULL
    ORDER BY {0} {1}
    """.format(sort_by, order_by)


    result = db.execute_query(query, (card_id,))
    
    # 关闭数据库连接
    db.close()

    # 格式化结果
    borrowed_books = []
    if not result:
        return borrowed_books
    for row in result:
        book = {
            'book_id': row[0],
            'category': row[1],
            'title': row[2],
            'press': row[3],
            'year': row[4],
            'author': row[5],
            'price': row[6],
            'total_nums': row[7],
            'stock': row[8]
        }
        borrowed_books.append(book)
    
    return borrowed_books

def borrow_book(card_id, book_id):
    """
    借书功能
    :param card_id: 借书证卡号
    :param book_id: 书号
    :return: 借书成功返回 True，失败返回 False
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    try:
        # 检查库存
        query = "SELECT stock FROM books WHERE book_id = ?"
        stock = db.execute_query(query, (book_id,))[0][0]

        if stock > 0:
            # 查询当前最大 record_id
            query_max_id = "SELECT MAX(record_id) FROM borrow_records"
            max_id_result = db.execute_query(query_max_id)
            next_id = max_id_result[0][0] + 1 if max_id_result[0][0] else 1

            # 更新库存
            update = "UPDATE books SET stock = stock - 1 WHERE book_id = ?"
            db.execute_update(update, (book_id,))

            # 添加借书记录
            borrow = """
            INSERT INTO borrow_records (record_id, book_id, card_id, borrow_date, admin_id)
            VALUES (?, ?, ?, ?, ?)
            """
            borrow_date = datetime.now().strftime("%Y-%m-%d")
            # 设置经办人
            current_seconds = int(datetime.now().strftime("%S"))
            if current_seconds % 20 < 5 and current_seconds % 20 >= 0:
                admin_id = 1
            elif current_seconds % 20 < 10 and current_seconds % 20 >= 5:
                admin_id = 2
            elif current_seconds % 20 < 15 and current_seconds % 20 >= 10:
                admin_id = 3
            elif current_seconds % 20 < 20 and current_seconds % 20 >= 15:
                admin_id = 4
            db.execute_insert(borrow, (next_id, book_id, card_id, borrow_date, admin_id)) 

            print("借书成功！")
            return True
        else:
            # 查询最近归还时间
            return_query = """
            SELECT MAX(return_date) FROM borrow_records WHERE book_id = ?
            """
            return_date = db.execute_query(return_query, (book_id,))[0][0]
            if return_date:
                print(f"该书无库存，最近归还时间为：{return_date}")
            else:
                print("该书无库存，且无归还记录。")
            return False
    except Exception as e:
        print("借书失败：", e)
        return False
    finally:
        # 关闭数据库连接
        db.close()

def test_borrow_book():
    """
    测试借书功能
    """
    # 输入借书证卡号
    card_id = "1"
    borrowed_books = get_borrowed_books(card_id)
    print(f"借书证 {card_id} 已借书籍：")
    if borrowed_books:
        for book in borrowed_books:
            print(book)
    else:
        print("无已借书籍。")

    # 输入书号
    book_id = "1"
    if borrow_book(card_id, book_id):
        print("借书操作成功完成！")
    else:
        print("借书操作失败。")

if __name__ == "__main__":
    # 运行测试
    test_borrow_book()