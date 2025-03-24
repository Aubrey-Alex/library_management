from utils.db_connector import DBConnector

def insert_query(db, book_info):
    """
    插入图书信息到数据库
    """
    # 读取数据
    category = book_info["category"].strip()
    title = book_info["title"].strip()
    press = book_info["press"].strip()
    year = int(book_info["year"])
    author = book_info["author"].strip()
    price = float(book_info["price"])

    # 查询是否已经有该书籍
    query = "SELECT * FROM books WHERE title = ? AND author = ? AND year = ? AND press = ? AND price = ? AND category = ?"
    params = (book_info["title"], book_info["author"], book_info["year"], book_info["press"], book_info["price"], book_info["category"])
    result = db.execute_query(query, params)

    # 如果已经有该书籍，则更新库存
    if len(result) > 0:
        book_id = result[0][0]
        current_total_nums = result[0][7]
        current_stock = result[0][8]
        total_nums = current_total_nums + int(book_info["total_nums"])
        stock = current_stock + int(book_info["total_nums"])
        para = (total_nums, stock, book_id)
        # SQL 更新语句
        insert = """
        UPDATE books SET total_nums = ?, stock = ? WHERE book_id = ?
        """
        print("更新图书信息：", insert, para)
    else:
        # 如果没有该书籍，则插入新书籍
        query = "SELECT MAX(book_id) FROM books"
        result = db.execute_query(query)
        if len(result) > 0 and result[0][0] is not None:
            book_id = result[0][0] + 1
        else:
            book_id = 1
        current_total_nums = 0
        current_stock = 0
        total_nums = current_total_nums + int(book_info["total_nums"])
        stock = current_stock + int(book_info["total_nums"])
        para = (book_id, category, title, press, year, author, price, total_nums, stock)
        # SQL 插入语句
        insert = """
        INSERT INTO books (book_id, category, title, press, year, author, price, total_nums, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        print("插入新图书：", insert, para)

    return insert, para

# 单本导入
def add_book(book_info):
    """
    添加单本图书到数据库
    """
    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    # 调用插入函数
    query, para = insert_query(db, book_info)
    db.execute_insert(query, para)

    # 关闭数据库连接
    db.close()

# 批量导入
def add_books(file):
    """
    批量添加图书到数据库
    :input: 输入格式为(书号, 类别, 书名, 出版社, 年份, 作者, 价格, 数量)  
    """
    # 读取数据
    books_infos = read_data(file)

    # 初始化数据库连接器
    db = DBConnector()
    db.connect()

    for book_info in books_infos:
        print("book_info:", book_info)
        # 调用插入函数
        query, para = insert_query(db, book_info)
        db.execute_insert(query, para)
        
    # 关闭数据库连接
    db.close()

# 读取数据
def read_data(file):
    """
    读取数据
    :input: 输入格式为(类别, 书名, 出版社, 年份, 作者, 价格, 数量)
    :output: 输出格式为列表，每个元素为图书信息元组(category, title, press, year, author, price, total_nums, stock)
    """
    books_infos = []
    # 读取数据
    with open(file.filename, 'r', encoding='utf-8') as file:
        # 检查file是否为txt或者docx文件
        if (file.name.endswith('.txt') or file.name.endswith('.docx')):
            for line in file:
                # 去除行末的换行符
                line = line.strip()
                # 使用逗号分隔数据
                data = line.split(',')
                if len(data) == 7:
                    # 将数据转换为元组并添加到列表中
                    title = data[0].strip()
                    author = data[1].strip()
                    press = data[2].strip()
                    year = int(data[3])
                    category = data[4].strip()
                    price = float(data[5])
                    total_nums = int(data[6])
                    book_info = {
                        "category": category,
                        "title": title,
                        "press": press,
                        "year": year,
                        "author": author,
                        "price": price,
                        "total_nums": total_nums
                    }
                    books_infos.append(book_info)
    return books_infos


def test_add_book():
    """
    测试 add_book 函数
    """

    # 调用 add_book 函数插入数据
    add_books()
    print("图书入库测试完成！")

if __name__ == "__main__":
    # 运行测试
    test_add_book()