from flask import Flask, render_template, request, redirect, url_for, session, jsonify  
from utils.db_connector import DBConnector
from utils.administrator_login import administrator_login
from models.search_book import default_books, search_books
from models.borrow_book import borrow_book, get_borrowed_books
from models.return_book import return_book
from models.add_book import add_book, add_books
from models.borrowers_admin import insert_borrower, delete_borrower, search_borrowers, default_borrowers
from models.book_info import total_books_query, borrowed_books_query, accumulated_borrowed_books_query

app = Flask(__name__)
app.secret_key = '3b9f8a7c5d6e4f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f'  # 设置会话密钥

# 首页
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['role'] == 'admin':
            admin_id = request.form['admin_id']
            password = request.form['password']
            # 调用登录验证函数
            if administrator_login(admin_id, password):
                session['admin_id'] = admin_id  # 将管理员ID存入会话
                return redirect(url_for('admin_dashboard'))  # 跳转到管理员面板
            else:
                return "登录失败，请检查管理员ID和密码。"
        else:
            return redirect(url_for('user_dashboard'), code=307)  # 跳转到首页
    return render_template('index.html')

# 管理员面板
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' in session:  # 检查是否已登录
        total_books = total_books_query()
        borrowed_books = borrowed_books_query()
        accumulated_borrowed_books = accumulated_borrowed_books_query()
        return render_template('admin_dashboard.html', total_books=total_books, borrowed_books=borrowed_books, accumulated_borrowed_books=accumulated_borrowed_books)
    else:
        return redirect(url_for('login'))  # 未登录则跳转到登录页面

# 退出登录
@app.route('/logout')
def logout():
    session.pop('admin_id', None)  # 清除会话中的管理员ID
    return redirect(url_for('index'))  # 跳转到登录页面

# 用户面板
@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    return render_template('user_dashboard.html')
    
# 图书入库
@app.route('/add_book', methods=['GET', 'POST'])
def route_add_book():
    if request.method == 'POST':
        book_info = {
            "category": request.form['category'],
            "title": request.form['title'],
            "press": request.form['press'],
            "year": request.form['year'],
            "author": request.form['author'],
            "price": request.form['price'],
            "total_nums": request.form['copies']
        }
        add_book(book_info)
        return redirect(url_for('admin_dashboard'))  # 跳转到管理员面板
    return render_template('index.html')

# 批量导入
@app.route('/batch_import', methods=['GET', 'POST'])
def batch_import():
    if request.method == 'POST':
        file = request.files['book_file']
        if file:
            add_books(file)
            return redirect(url_for('admin_dashboard'))  # 跳转到管理员面板
    return redirect(url_for('admin_dashboard'))

# 借书证管理
@app.route('/manage_borrowers', methods=['GET', 'POST'])
def manage_borrowers():
    if request.method == 'POST':
        if "insert_borrower" in request.form:
            name = request.form['name']
            workplace = request.form['workplace']
            type = request.form['borrower-category']
            insert_borrower(name, workplace, type)
        elif "delete_borrower" in request.form:
            card_id = request.form['card_id']
            name = request.form['name']
            delete_borrower(card_id, name)
        elif "search_borrower" in request.form or request.is_json:
            # Handle AJAX requests for search or default data
            if request.is_json:
                data = request.get_json()
                name = data.get('search_borrower_name', '')
            else:
                name = request.form.get('search_borrower_name', '')
            
            if name:
                # Search borrowers by name
                borrowers = search_borrowers(name)
            else:
                # Get default borrowers (limit 3)
                borrowers = default_borrowers()
            
            # If it's an AJAX request, return JSON
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(borrowers)
            
            # Otherwise, render the full page
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('admin_dashboard'))  
    return redirect(url_for('admin_dashboard'))
    
# 图书查询
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # 解析 JSON 数据
        if request.is_json:
            data = request.get_json()
        else:  # 兼容表单数据
            data = request.form

        # 获取查询条件
        conditions = {
            "title": data.get('title'),
            "author": data.get('author'),
            "category": data.get('category'),
            "year_start": data.get('year_start'),
            "year_end": data.get('year_end'),
            "price_min": data.get('price_min'),
            "price_max": data.get('price_max')
        }

        if not any(conditions.values()):  # 如果没有任何查询条件，则显示默认数据
            books = default_books()
        else:
            books = search_books(conditions, data.get('sort_by'), data.get('order_by'))

        # 检测请求类型并返回相应数据
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(books)  # 最多返回 50 条数据

        return redirect(url_for('search'))
    return redirect(url_for('search'))

# 借书
@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    if request.method == 'POST':
        if "search_borrowed_books" in request.form or request.is_json:
            # Handle AJAX requests for search or default data
            if request.is_json:
                data = request.get_json()
                card_id = data.get('card_id', '')
                sort_by = data.get('sort_by', 'title')
                order_by = data.get('order_by', 'asc')
            else:
                card_id = request.form.get('card_id', '')
                sort_by = request.form.get('sort_by', 'title')
                order_by = request.form.get('order_by', 'asc')
            
            if card_id:
                # Search borrowed books by card ID
                result = get_borrowed_books(card_id, sort_by, order_by)
            else:
                # Get default borrowed books
                result = default_books()
            
            # If it's an AJAX request, return JSON
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(result)
            
            # Otherwise, render the full page
            return redirect(url_for('user_dashboard'))
        elif "borrow_book" in request.form:
            card_id = request.form['card_id']
            book_id = request.form['book_id']
            borrow_book(card_id, book_id)
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('user_dashboard'))
        
# 还书
@app.route('/returns', methods=['GET', 'POST'])
def returns():
    if request.method == 'POST':
        if "search_borrowed_books" in request.form or request.is_json:
            # Handle AJAX requests for search or default data
            if request.is_json:
                data = request.get_json()
                card_id = data.get('card_id', '')
                sort_by = data.get('sort_by', 'title')
                order_by = data.get('order_by', 'asc')
            else:
                card_id = request.form.get('card_id', '')
                sort_by = request.form.get('sort_by', 'title')
                order_by = request.form.get('order_by', 'asc')
            
            if card_id:
                # Search borrowed books by card ID
                result = get_borrowed_books(card_id, sort_by, order_by)
            else:
                # Get default borrowed books
                result = default_books()
            
            # If it's an AJAX request, return JSON
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(result)
            
            # Otherwise, render the full page
            return redirect(url_for('user_dashboard'))
        elif "return_book" in request.form:
            card_id = request.form['card_id']
            book_id = request.form['book_id']
            print("还书结果：", return_book(card_id, book_id))
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('user_dashboard'))





if __name__ == '__main__':
    app.run(debug=True)