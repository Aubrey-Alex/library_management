from utils.db_connector import DBConnector
from datetime import datetime

def get_borrowed_books(card_id):
    """
    获取某借书证所有已借书籍（app.py中未使用）
    :param card_id: 借书证卡号
    :return: 已借书籍列表
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    # SQL 查询语句
    query = """
    SELECT b.book_id, b.title, b.author, br.borrow_date, br.return_date
    FROM borrow_records br
    JOIN books b ON br.book_id = b.book_id
    WHERE br.card_id = ? AND br.return_date IS NULL
    """

    # 执行查询
    result = db.execute_query(query, (card_id,))
    
    # 关闭数据库连接
    db.close()

    return result

def return_book(card_id, book_id):
    """
    还书功能
    :param card_id: 借书证卡号
    :param book_id: 书号
    :return: 还书成功返回 True，失败返回 False
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    try:
        # 检查该书是否在已借书籍列表中
        query = """
        SELECT * FROM borrow_records
        WHERE card_id = ? AND book_id = ? AND return_date IS NULL
        """
        result = db.execute_query(query, (card_id, book_id))

        if result:
            # 更新库存
            update_query = "UPDATE books SET stock = stock + 1 WHERE book_id = ?"
            db.execute_update(update_query, (book_id,))

            # 更新借书记录（设置还书日期）
            return_query = """
            UPDATE borrow_records SET return_date = ?
            WHERE card_id = ? AND book_id = ? AND return_date IS NULL
            """
            return_date = datetime.now().strftime("%Y-%m-%d")
            db.execute_update(return_query, (return_date, card_id, book_id))
            return (f"还书成功！归还日期：{return_date}，欢迎下次借阅。")
        else:
            return "还书失败：您未借阅该书籍。"
    except Exception as e:
        return ("还书失败:", e)
    finally:
        # 关闭数据库连接
        db.close()

def test_return_book():
    """
    测试还书功能
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
    if return_book(card_id, book_id):
        print("还书操作成功完成！")
    else:
        print("还书操作失败。")

if __name__ == "__main__":
    # 运行测试
    test_return_book()