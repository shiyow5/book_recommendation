from collections import deque, defaultdict

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size
        self.graph = defaultdict(list)  # グラフを追加

    def find(self, p): # O(α(n)), α()は逆アッカーマン関数
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q): # O(α(n))
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP != rootQ:
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1
        # グラフにエッジを追加
        self.graph[p].append(q)
        self.graph[q].append(p)

    def connected(self, p, q): # O(α(n))
        return self.find(p) == self.find(q)
    
    def custom_connected(self, p, q, dis=2): # O(|V|+|E|)
        return (self.find(p) == self.find(q)) and (self.distance(p, q) <= dis)

    def distance(self, start, end): # O(|V|+|E|)
        if not self.connected(start, end):
            return -1  # 連結していない場合は -1 を返す
        if start == end:
            return 0

        visited = [False] * len(self.parent)
        queue = deque([(start, 0)])  # (ノード, 距離)

        while queue:
            current, dist = queue.popleft()
            if current == end:
                return dist
            for neighbor in self.graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, dist + 1))

        return -1  # 経路が見つからない場合（通常はあり得ない）
"""
# とりあえず手入力
N = 8  # ユーザー数
R = 7  # 友達関係の数
relations = [
    (8, 6),
    (1, 2),
    (1, 4),
    (1, 6),
    (6, 7),
    (7, 8),
    (3, 5),
]

Q = 6  # 質問の数
queries = [
    (1, 2),
    (1, 3),
    (1, 8),
    (1, 5),
    (5, 6),
    (6, 5),
]
"""
def str2uf(str_data):
    n, _ = map(int, str_data[0].split())
    relations = []
    str_data.pop(0)
    for s in str_data:
        relation = list(map(int, s.split()))
        #print(relation)
        if len(relation) != 2:
            raise Exception('This is not appropriate data.')
        relations.append(relation)

    # 初期化
    uf = UnionFind(n + 1)  # ユーザーは1-indexedなので+1

    # 友達関係を追加
    for s, t in relations:
        uf.union(s, t)

    return uf

def str2q(str_data):
    queries = []
    str_data.pop(0)
    for q in str_data:
        querie = list(map(int, q.split()))
        if len(querie) != 2:
            raise Exception('This is not appropriate question.')
        queries.append(querie)
    
    return queries

def judge(uf, queries):
    # クエリの処理
    results = []
    for p, q in queries:
        if uf.connected(p, q):
            results.append("yes")
        else:
            results.append("no")
        #ここでresultsは完成
    return results

if (__name__ == '__main__'):
    file1_name = 'ex05_test1.txt' # テスト用のファイル名を設定
    file2_name = 'ex05_test2.txt'
    data1_path = __file__.replace('ex05.py', 'Test_data/'+file1_name)
    data2_path = __file__.replace('ex05.py', 'Test_data/'+file2_name)

    with open(data1_path) as data1, open(data2_path) as data2:
        str_data1 = data1.readlines()
        str_data2 = data2.readlines()
    uf = str2uf(str_data1)
    queries = str2q(str_data2)

    results = judge(uf, queries)

    for result in results:
        print(result)
        
    for i in range(1,9):
        for j in range(i+1,9):
            print(f"({i},{j}): {uf.distance(i, j)}")
