#2つのベクトルの類似度を0~1の値で出力
def vector_similarity(vec1=[0], vec2=[0]):
    if (len(vec1) != len(vec2)):#配列の大きさが一致していないとエラー
        raise Exception('Vector length error')
        
    distance = 0
    for i in range(len(vec1)):
        if (vec1[i]!=-1.0 and vec2[i]!=-1.0):
            distance += (vec1[i] - vec2[i])**2
    distance = distance**(1/2)
    
    similarity = 1 / (distance + 1)
    
    return similarity #int




#ターゲットユーザIDと全ユーザの書籍評価データを引数に類似ユーザのリストを取得
def similarity_list(target=1, evals={1:[0], 2:[0]}, sort=False):
    if (not(target in evals)):
        raise Exception('User not found')
    
    if (len(evals) < 2):
        raise Exception('Lack of data length')
    
    sim_data = {}
    for user in evals.keys():
        if (target == user):
            continue
        sim_data[user] = vector_similarity(evals[target], evals[user])
        
    sorted_list = sorted(sim_data.items(), key = lambda x : x[1], reverse=True)
    
    if (sort is False):
        return sim_data #dice
    elif (sort is True):
        return sorted_list #list

#データ読み取り
def scan_Data():
    n, m = map(int, input().split())
    
    user_lists = {}
    for i in range(n):
        book_ratings = list(map(float, input().split()))
        
        if (len(book_ratings) != m):
            return {1:["Error"], 2:["Error"]}
        
        user_lists[i+1] = (book_ratings)
        
    return user_lists #dict

"""def main():
    default_user = 1
    
    data = scan_Data()
    
    SimUser_list = similarity_list(default_user, data, sort=True)
    
    if (type(SimUser_list) == list):
        print("<UserID> <Similarity>")
        for SimUser in SimUser_list:
            print(f"{SimUser[0]} {SimUser[1]}")
    else:
        print(SimUser_list)


if (__name__ == "__main__"):
    main()
"""
