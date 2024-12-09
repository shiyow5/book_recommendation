from flask import Flask, render_template, request, redirect, url_for, session
import os
from ..Phase2.ex07 import unpack
from ..Phase3.ex09 import *

current_file_path = os.path.abspath(__file__)
SOURCE_DIR = current_file_path.replace(os.path.join('code', 'GUI', 'app.py'), os.path.join('source/'))

app = Flask(__name__)
app.secret_key = 'sato_sho_key' # セッションを使うための秘密鍵を設定

books = {}
users = {}

# 書籍データ
def init_books():
    global books
    save_source(unpack())
    dbo = BookDBO()
    book_datas = dbo.search(table_name='book')
    books = {bid+1: {'title': data[1], 'url': data[2], 'ratings': {}} for bid, data in enumerate(book_datas)}
    dbo.close()

# フレンドデータ
def init_friend():
    global users
    dbo = UserDBO()
    dbo.update_friend()
    user_datas = dbo.search(table_name='user')
    users = {}
    for user_data in user_datas:
        user = user_data[1]
        friend_datas = [f[0] for f in dbo.get_friend(user)]
        users[user] = {'friends': friend_datas}
        
init_books()
init_friend()


@app.route('/', methods=['GET', 'POST'])
def login():
    global books, users
    if request.method == 'POST':
        dbo = UserDBO()
        # ログイン処理 (ここでは簡易的にユーザー名とパスワードをチェック)
        username = request.form['username']
        password = request.form['password']
        
        if username != 'administrator':
            userdata = dbo.search(table_name='user', values={'user': username})
            if userdata:
                userdata = userdata[0]
            else:
                return render_template('login.html', error='ユーザー名またはパスワードが違います。')
            # 元からある評価を読み込み
            for bid in books.keys():
                rating = dbo.search(table_name='eval', values={'userid': userdata[0], 'bookid': bid})
                if rating:
                    rating = rating[0][3]
                    books[bid]['ratings'][username] = rating
        dbo.close()
        
        if username == 'administrator' and password == 'satosho': # べた書きですまねぇ
            session['logged_in'] = True  # ログイン状態をセッションに保存
            session['user_name'] = username
            return render_template('manage_books.html')
        elif userdata[2] == password:
            session['logged_in'] = True
            session['user_name'] = username
            return redirect(url_for('search'))
        else:
            return render_template('login.html', error='ユーザー名またはパスワードが違います。')
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    """セッションをクリアしてログアウト処理を行う"""
    session.pop('logged_in', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    global books, users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='そのユーザー名はすでに使用されています。')
        else:
            users[username] = {'friends': [], 'password': password} # パスワードも保存
            session['logged_in'] = True
            session['user_name'] = username
            dbo = UserDBO()
            dbo.insert(table_name='user', values={'user': username, 'password': password})
            dbo.close()
            return redirect(url_for('search'))
    else:
        return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    global books, users
    if 'logged_in' in session:
        query = request.args.get('query', '')
        matched_books = []
        if query:
            dbo = BookDBO()
            searcheds = search_from_db(query)
            if searcheds:
                for searched in searcheds.keys():
                    searched_id = dbo.search(table_name='book', values={'url': searched})[0][0] # search_from_db()からの戻り値なので必ず検索で帰ってくる
                    matched_books.append(searched_id)
            dbo.close()
        else:
            matched_books = list(books.keys())  # 全ての書籍を表示

        if request.method == 'POST':
            dbo = UserDBO()
            user_id = dbo.search(table_name='user', values={'user': session.get('user_name')})
            if user_id:
                user_id = user_id[0][0]

            # 評価処理
            book_id = int(request.form['book_id'])
            rating = int(request.form['rating'])
            books[book_id]['ratings'][session.get('user_name')] = rating
            dbo.delete(table_name='eval', values={'userid': str(user_id), 'bookid': str(book_id)})
            dbo.insert(table_name='eval', values={'userid': str(user_id), 'bookid': str(book_id), 'eval': str(rating)})
            dbo.close()
            # 同じページにリダイレクトして再表示
            return redirect(url_for('search', query=query))

        return render_template('search.html', books={book_id: books[book_id] for book_id in matched_books}, query=query)
    else:
        return redirect(url_for('login'))
    
@app.route('/recommend')
def recommend():
    global books, users
    if 'logged_in' in session:
        dbo = UserDBO()
        user_id = dbo.search(table_name='user', values={'user': session.get('user_name')})
        if user_id:
            user_id = user_id[0][0]
        dbo.close()
        
        dbo = BookDBO()
        # ここに推薦ロジックを実装
        try:
            recommend_datas = get_recommendation_from_db(user_id)
        except Exception:
            recommend_datas = []
            
        recommended_books = {}
        for i, recomend_data in enumerate(recommend_datas):
            book_name = dbo.search(table_name='book', values={'rowid': str(recomend_data[0])})
            if book_name:
                recommended_books[i+1] = {'title': book_name[0][1], 'url':book_name[0][2]}
        dbo.close()
                
        if not recommended_books:
            recommended_books = {
                1: {'title': '推薦できる図書がありません', 'url': 'Error'},
            }
        
        return render_template('recommend.html', books=recommended_books)
    else:
        return redirect(url_for('login'))
    

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    global books, users
    if 'logged_in' in session:
        current_user = session.get('user_name')
        if request.method == 'POST':
            query = request.form.get('query', '').lower()
            matched_users = [user for user in users if (query in user.lower()) and (session.get('user_name').lower() != user.lower())]
            #  マッチしたユーザー一覧を渡す際に、フレンド関係も伝える
            user_data = []
            for user in users.keys():
                if user in matched_users:
                    is_friend = user in users[current_user]['friends']
                    user_data.append({'username': user, 'is_friend': is_friend})
        else:
            #  ユーザー一覧を渡す際に、フレンド関係も伝える
            user_data = []
            for user in users.keys():
                if session.get('user_name').lower() != user.lower():
                    is_friend = user in users[current_user]['friends']
                    user_data.append({'username': user, 'is_friend': is_friend})
        
        return render_template('friends.html', users=user_data) 
    
    else:
        return redirect(url_for('login'))
    
@app.route('/add_friend', methods=['POST'])
def add_friend():
    global books, users
    if 'logged_in' in session:
        current_user = session.get('user_name')
        friend_to_add = request.form['user']
        if friend_to_add in users and current_user in users:  
            if friend_to_add not in users[current_user]['friends']:
                # こちらがフレンドに追加したら相手からも自分がフレンドになる
                users[current_user]['friends'].append(friend_to_add)
                users[friend_to_add]['friends'].append(current_user)
                dbo = UserDBO()
                user_id = dbo.search(table_name='user', values={'user': current_user})[0][0]
                friend_id = dbo.search(table_name='user', values={'user': friend_to_add})[0][0]
                dbo.insert(table_name='friend_link', values={'userid': str(user_id), 'friend': str(friend_id)})
                dbo.update_friend()
                dbo.close()
            return redirect(url_for('friends'))
        else:
            return "ユーザーが見つかりません", 400  
    else:
        return redirect(url_for('login'))
    
    
@app.route('/delete_friend', methods=['POST'])
def delete_friend():
    if 'logged_in' in session:
        current_user = session.get('user_name')
        friend_to_delete = request.form['user']
        if friend_to_delete in users and current_user in users:
            if friend_to_delete in users[current_user]['friends']:
                users[current_user]['friends'].remove(friend_to_delete)
                users[friend_to_delete]['friends'].remove(current_user)
                dbo = UserDBO()
                user_id = dbo.search(table_name='user', values={'user': current_user})[0][0]
                friend_id = dbo.search(table_name='user', values={'user': friend_to_delete})[0][0]
                dbo.delete(table_name='friend_link', values={'userid': user_id, 'friend': friend_id})
                dbo.delete(table_name='friend_link', values={'userid': friend_id, 'friend': user_id})
                dbo.update_friend()
                dbo.close()
        return redirect(url_for('friends'))
    else:
        return redirect(url_for('login'))
    

@app.route('/manage_books', methods=['GET', 'POST'])
def manage_books():
    """書籍管理ページの処理"""
    global books, users

    # ログイン済みで、かつ管理者(user_id='admin')の場合のみアクセス許可
    if 'logged_in' in session and session.get('user_name') == 'administrator':
        if request.method == 'POST':
            # 書籍追加
            if 'add_book' in request.form:
                book_name = request.form['book_name']
                document_content = request.form['document_content']
                
                # 書籍名が入力されているかチェック
                if book_name:
                    # 書籍データに追加
                    with open(SOURCE_DIR+book_name+'.html', 'w') as data:
                        data.write(document_content)
                    init_books()
                    return render_template('manage_books.html', message=f'書籍 "{book_name}" が追加されました')
                else:
                    return render_template('manage_books.html', error='書籍名を入力してください')

            # 書籍削除
            if 'delete_book' in request.form:
                book_name = request.form['book_name'] + '.html'
                # 書籍が存在するかチェック
                if book_name in os.listdir(SOURCE_DIR):
                    os.remove(os.path.join(SOURCE_DIR, book_name))
                    book_name = book_name.replace('.html', '')
                    dbo = BookDBO()
                    book_id = dbo.search(table_name='book', values={'book': book_name})[0][0]
                    dbo.close()
                    dbo = UserDBO()
                    dbo.delete(table_name='eval', values={'bookid': book_id})
                    dbo.close()
                    init_books()
                    return render_template('manage_books.html', message=f'書籍 "{book_name}" が削除されました')
                else:
                    return render_template('manage_books.html', error='書籍が見つかりません')

        # GETリクエスト、または処理後の場合は書籍管理ページを表示
        return render_template('manage_books.html')
    else:
        # ログインしていない、または管理者でない場合はログインページへリダイレクト
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

# アプリの実行
# gunicorn code.GUI.app:app
# データベースの初期化など
# python -m code.Phase3.ex09