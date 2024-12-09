from . import ex01

def User2Book(evals:dict)->dict:
    '''
    カラムをユーザではなく書籍に変換(行列とみなした時の転置)
    '''
    
    converted = {}
    for bid in range(1, len(evals[1])+1):
        converted[bid] = []
        for uid in evals.keys():#range(1, len(evals)+1):
            converted[bid].append(evals[uid][bid-1])
    
    return converted

def recommendation(target:int, evals:dict, sort:bool=True, exclude:list=[]):
    '''
    targetに対する推薦書籍一覧を返す
    sortがTrueであれば結果を降順で返す
    '''    
    
    book_data = User2Book(evals)
    
    #book_idではない(id-1の値)
    for bid in range(1, len(evals[target])+1):
        if (evals[target][bid-1] != -1.0):     #ターゲットユーザが評価してない書籍に絞る
            book_data.pop(bid, None)
            
    if (not book_data):
        raise Exception('Not item recommended.')
            
    sim_score = ex01.similarity_list(target, evals, sort=False)
    
    recommendations = book_data.copy()    #推薦度: 重み付き評価
    
    for book_id in recommendations.keys():
        for user_id in sim_score.keys():
            if (recommendations[book_id][user_id-1] != -1.0):
                recommendations[book_id][user_id-1] *= sim_score[user_id]    #重み付き評価を計算
            if (user_id in exclude):
                recommendations[book_id][user_id-1] = -1.0    #excludeの処理
                
        
    S_par_A = {}
    for book_id in recommendations.keys():
        recommendation_sum = sum(r for r in recommendations[book_id] if r != -1.0)    #各書籍の推薦度を合計
        score_sum = sum(s for i, s in sim_score.items() if recommendations[book_id][i-1] != -1.0)    #上の書籍を評価したユーザの類似スコアを合計
        if (score_sum != 0):    #All friend not evaluate this bookの場合を除外
            S_par_A[book_id] = recommendation_sum / score_sum    #総合推薦度を計算
        else:
            S_par_A[book_id] = 0    #誰も評価していない場合は推薦はするが総合推薦度は0として出力
        
    sorted_list = sorted(S_par_A.items(), key = lambda x : x[1], reverse=True)    #結果をソート
    
    if (sort is False):
        return S_par_A
    elif (sort is True):
        return sorted_list

def test(data):
    '''
    すべてのidに対してrecommendation()を実行し、結果を表示する
    '''
    
    results = {}
    
    for id in range(1, len(data)+1):
        try:
            _data = recommendation(id, data, True)
            print(f'id:{id}\n{_data}')
        except Exception as e:
            print(f'id:{id}\n{e}')
            continue
        
        results[id] = _data
        
    '''
    print('EXCLUDE TEST')
    for id in range(1, len(data)+1):
        try:
            _data = recommendation(id, data, exclude=[3,5])
            print(f'id:{id}(exclude user=3,5)\n{_data}')
        except Exception as e:
            print(f'id:{id}\n{e}')
            continue
    '''
        
    return results

def str2dict(str_data):
    '''
    文字列での入力データを辞書型に変換する
    '''
    n, m = map(int, str_data[0].split())
    
    dict_data = {}
    for id in range(1, n+1):
        evals = list(map(float, str_data[id].split(' ')))
        
        if (len(evals) != m):
            raise Exception('This is not appropriate data.')
        
        dict_data[id] = evals
        
    return dict_data