import os
import sqlite3
from ..Phase1.ex02 import recommendation
from ..Phase1.ex03 import convert_data
from ..Phase2.ex05 import *
from ..Phase2.ex06 import notfriend
from ..Phase2.ex07 import *
from ..Phase2.ex08 import search_keyword


class DBOperation:
    def __init__(self, db_name:str = "info.db", new:bool=False):
        self.DB_NAME = db_name
        
        current_file_path = os.path.abspath(__file__)
        self.DB_PATH = current_file_path.replace(os.path.join('code', 'Phase3', 'ex09.py'), os.path.join('datas', db_name))
        
        if new and os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)
        
        if not os.path.exists(self.DB_PATH):
            with open(self.DB_PATH, 'w') as f:
                pass
            
        self.conn = sqlite3.connect(self.DB_PATH)
            
        
    def create(self, table_name:str, table_info:dict):
        cur = self.conn.cursor()
        
        query_values = [f"{value} {type}" for value, type in table_info.items()]
        
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(query_values)})"
        )
        
        cur.close()
        
    def search(self, table_name:str, values:dict=None):
        if (values):
            query_values = [f"{column} = '{value}'" for column, value in values.items()]
            where_query = f" WHERE {' AND '.join(query_values)}"
        else:
            where_query = ""
            
        result = self.custom_search(table_name=table_name, query=where_query)
        
        return result
    
    def custom_search(self, table_name:str, query:str=""):
        cur = self.conn.cursor()
        
        cur.execute(
            f"SELECT rowid,* FROM {table_name}" + query
        )
        
        result = cur.fetchall()
        cur.close()
        
        return result
        
    def insert(self, table_name:str, values:dict, duplicable:bool=False): # duplicable:重複可能かどうか
        cur = self.conn.cursor()
        
        if ((not self.search(table_name, values)) or duplicable):
            cur.execute(
                f"""INSERT INTO {table_name} ({', '.join(values.keys())}) VALUES ("{'", "'.join(values.values())}")"""
            )
        
        self.conn.commit()
        cur.close()
    
    def delete(self, table_name:str, values:dict=None):
        cur = self.conn.cursor()
        
        if (values):
            query_values = [f"{column} = '{value}'" for column, value in values.items()]
            where_query = f" WHERE {' AND '.join(query_values)}"
        else:
            where_query = ""
        
        cur.execute(
            f"DELETE FROM {table_name}" + where_query
        )
        
        self.conn.commit()
        cur.close()
    
    def close(self):
        self.conn.close()


class SourceDBO(DBOperation):
    def __init__(self, db_name:str = "sourceinfo.db", new:bool=False):
        super().__init__(db_name=db_name, new=new)
        
        self.create(table_name='url', table_info={'url': 'varchar(100)'})
        self.create(table_name='word', table_info={'word': 'varchar(100)'})
        self.create(table_name='link', table_info={'source': 'int', 'target': 'int'})
        self.create(table_name='location', table_info={'wordid': 'int', 'urlid': 'int'})
        
    def contain_word(self, url:str):
        cur = self.conn.cursor()
        
        url_id = self.search(table_name='url', values={'url': url})
        if url_id:
            url_id = url_id[0][0]
        else:
            url_id = 0
        
        cur.execute(
            f"select word.word from url, word, location "
            f"where url.rowid=location.urlid and word.rowid=location.wordid and url.rowid='{url_id}';"
        )
        
        words = [word[0] for word in cur.fetchall()]
        
        cur.execute(
            f"select url.url from url, link "
            f"where link.source={url_id} and url.rowid=link.target"
        )
        
        words += [word[0] for word in cur.fetchall()]
        
        cur.close()
        
        return words
        
        
class UserDBO(DBOperation):
    def __init__(self, db_name:str = "userinfo.db", new:bool=False):
        super().__init__(db_name=db_name, new=new)
        
        self.create(table_name='user', table_info={'user': 'varchar(100)', 'password': 'varchar(100)'})
        self.create(table_name='friend_link', table_info={'userid': 'int', 'friend': 'int'})
        self.create(table_name='friend', table_info={'userid': 'int', 'friend': 'int'})
        self.create(table_name='eval', table_info={'userid': 'int', 'bookid': 'int', 'eval': 'float'})
        
    def update_friend(self):
        n = len(self.search(table_name='user'))
        uf = UnionFind(n+1)
        relations = self.search(table_name='friend_link')
        
        for relation in relations:
            uf.union(relation[1], relation[2])
            
        self.delete(table_name='friend')
            
        for id1 in range(1, n+1):
            for id2 in range(1, n+1):
                if (id1!=id2 and uf.custom_connected(id1, id2, 1)):
                    self.insert(table_name='friend', values={'userid': str(id1), 'friend': str(id2)})
        
    def get_friend(self, user:str):
        cur = self.conn.cursor()
        
        user_id = self.search(table_name='user', values={'user': user})
        if user_id:
            user_id = user_id[0][0]
        else:
            user_id = 0
        
        cur.execute(
            f"select user.user from user, friend "
            f"where friend.userid={user_id} and user.rowid=friend.friend"
        )
        
        friends = cur.fetchall()
        
        cur.close()
        
        return friends


class BookDBO(DBOperation):
    def __init__(self, db_name:str = "bookinfo.db", new:bool=False):
        super().__init__(db_name=db_name, new=new)
        
        self.create(table_name='book', table_info={'book': 'varchar(100)', 'url': 'varchar(100)'})

        
def save_source(source:dict):
    dbo = SourceDBO(new=True)
    
    # save url table
    urls = source.keys()
    for url in urls:
        dbo.insert(table_name='url', values={'url': url})
    
    # save word table
    words = list(set([item for sublist in source.values() for item in sublist if item not in urls]))
    for word in words:
        dbo.insert(table_name='word', values={'word': word})
    
    # save link table
    for url, wl in source.items():
        for w in wl:
            if (w in urls):
                l_from = str(dbo.search(table_name='url', values={'url': url})[0][0])
                l_to = str(dbo.search(table_name='url', values={'url': w})[0][0])
                dbo.insert(table_name='link', values={'source': l_from, 'target': l_to}, duplicable=True)
    
    # save location table
    for url, wl in source.items():
        for w in wl:
            if (w not in urls):
                i_from = str(dbo.search(table_name='word', values={'word': w})[0][0])
                i_to = str(dbo.search(table_name='url', values={'url': url})[0][0])
                dbo.insert(table_name='location', values={'wordid': i_from, 'urlid': i_to}, duplicable=True)
                
    # calc and save pagerank
    p = PageRank(source)
    p.score()
    page_score = p.get_score(normalization=False)
    dbo.create(table_name='pagerank', table_info={'urlid': 'int', 'score': 'float'})
    for url, score in page_score.items():
        urlid = str(dbo.search(table_name='url', values={'url': url})[0][0])
        dbo.insert(table_name='pagerank', values={'urlid': urlid, 'score': str(score)})
    
    dbo.close()
    
    dbo = BookDBO(new=True)
    for url in urls:
        dbo.insert(table_name='book', values={'book': url.replace('.html', ''), 'url': url})
    dbo.close()
    
    
def init_user():
    dbo = UserDBO(new=True)
    
    dbo.insert(table_name='user', values={'user': 'shishido', 'password': 'takumi'})
    dbo.insert(table_name='user', values={'user': 'kano', 'password': 'yushi'})
    dbo.insert(table_name='user', values={'user': 'sasaki', 'password': 'nozomi'})
    dbo.insert(table_name='user', values={'user': 'oomuro', 'password': 'keiya'})
    dbo.insert(table_name='user', values={'user': 'sato', 'password': 'sho'})
    dbo.insert(table_name='user', values={'user': 'usami', 'password': 'yuki'})
    dbo.insert(table_name='user', values={'user': 'aizu', 'password': 'taro'})
    dbo.insert(table_name='user', values={'user': 'guest', 'password': '123'})
    
    dbo.insert(table_name='friend_link', values={'userid': '1', 'friend': '2'})
    dbo.insert(table_name='friend_link', values={'userid': '1', 'friend': '4'})
    dbo.insert(table_name='friend_link', values={'userid': '1', 'friend': '6'})
    dbo.insert(table_name='friend_link', values={'userid': '6', 'friend': '7'})
    dbo.insert(table_name='friend_link', values={'userid': '7', 'friend': '8'})
    dbo.insert(table_name='friend_link', values={'userid': '3', 'friend': '5'})
    
    dbo.insert(table_name='eval', values={'userid': '1', 'bookid': '1', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '1', 'bookid': '2', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '2', 'bookid': '4', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '3', 'bookid': '1', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '3', 'bookid': '2', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '3', 'bookid': '3', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '3', 'bookid': '4', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '3', 'bookid': '5', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '4', 'bookid': '1', 'eval': '1.0'})
    dbo.insert(table_name='eval', values={'userid': '4', 'bookid': '2', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '4', 'bookid': '5', 'eval': '4.0'})
    dbo.insert(table_name='eval', values={'userid': '5', 'bookid': '1', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '5', 'bookid': '2', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '5', 'bookid': '3', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '6', 'bookid': '1', 'eval': '4.0'})
    dbo.insert(table_name='eval', values={'userid': '6', 'bookid': '2', 'eval': '3.0'})
    dbo.insert(table_name='eval', values={'userid': '6', 'bookid': '3', 'eval': '3.0'})
    dbo.insert(table_name='eval', values={'userid': '6', 'bookid': '4', 'eval': '3.0'})
    dbo.insert(table_name='eval', values={'userid': '6', 'bookid': '5', 'eval': '3.0'})
    dbo.insert(table_name='eval', values={'userid': '7', 'bookid': '2', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '7', 'bookid': '3', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '7', 'bookid': '4', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '7', 'bookid': '5', 'eval': '1.0'})
    dbo.insert(table_name='eval', values={'userid': '8', 'bookid': '1', 'eval': '5.0'})
    dbo.insert(table_name='eval', values={'userid': '8', 'bookid': '2', 'eval': '2.0'})
    dbo.insert(table_name='eval', values={'userid': '8', 'bookid': '3', 'eval': '1.0'})
    dbo.insert(table_name='eval', values={'userid': '8', 'bookid': '4', 'eval': '3.0'})
    dbo.insert(table_name='eval', values={'userid': '8', 'bookid': '5', 'eval': '5.0'})
    
    dbo.close()
    

def get_recommendation_from_db(target:int):
    dbo = BookDBO()
    M = len(dbo.search(table_name='book'))
    dbo.close()
    
    dbo = UserDBO()
    N = len(dbo.search(table_name='user'))

    eval_datas = dbo.search(table_name='eval')
    E = len(eval_datas)
    eval_datas = [[N, M, E]] + [[data[1], data[2], data[3]] for data in eval_datas]
    eval_datas = convert_data(eval_datas)
    
    friend_datas = dbo.search(table_name='friend_link')
    R = len(friend_datas)
    friend_datas = [f"{N} {R}"] + [f"{data[1]} {data[2]}" for data in friend_datas]
    friend_uf = str2uf(friend_datas)
    
    exclude = notfriend(friend_uf, eval_datas, target)
    rec = recommendation(target, eval_datas, True, exclude)
    
    dbo.close()
    
    return rec


def search_from_db(keyword:str):
    dbo_b = BookDBO()
    dbo_s = SourceDBO()
    
    pack = {}
    for book_data in dbo_b.search(table_name='book'):
        url = book_data[1]+'.html'
        pack[url] = dbo_s.contain_word(url)
        
    dbo_b.close()
    dbo_s.close()
    
    p = PageRank(pack)
    p.score()
    page = p.get_score(True)
    
    keyword = list(set(keyword.split()))
    word = search_keyword(pack, keyword)
    # score = {key: (word[key] + page[key]) for key in word.keys()}
    score = {key: (word[key] + page[key]) for key in word.keys() if word[key]}
    # 検索ワードと全く関連のないページは表示されないようにした
    sorted_keys = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))
    
    return sorted_keys


def main():
    save_source(unpack())
    init_user()
    result1 = get_recommendation_from_db(1)
    print(result1)
    
    result2 = search_from_db('list queue bfs list')
    print(result2)
    
    dbo = UserDBO()
    dbo.update_friend()
    print(dbo.get_friend('shishido'))
   

if (__name__ == "__main__"):
    main()
