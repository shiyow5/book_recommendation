from . import ex02

def convert_data(b_history:list):

    n = b_history[0][0]
    m = b_history[0][1]
    e = b_history[0][2]
    
    user_lists = [[-1.0 for _ in range(m)] for _ in range(n)]
    for i in range(e):
        user = int(b_history[i+1][0])
        book = int(b_history[i+1][1])
        point= b_history[i+1][2]
        
        user_lists[user-1][book-1] = point
    
    converted = {}
    for i in range(n):
        converted[i+1] = user_lists[i]

    return converted

def str2list(str_data):
    '''
    文字列での入力データを辞書型に変換する
    '''
    n, m, e = map(int, str_data[0].split())
    
    list_data = [[0 for _ in range(3)] for _ in range(e+1)]
    for id in range(e+1):
        if (id == 0):
            list_data[id][0], list_data[id][1], list_data[id][2] = n, m, e
        else:
            list_data[id][0], list_data[id][1], list_data[id][2] = map(float, str_data[id].split())
        
    return list_data

if (__name__ == '__main__'):
    file_name = 'ex03_test.txt' # テスト用のファイル名を設定
    data_path = __file__.replace('ex03.py', 'Test_data/'+file_name)
    
    try:
        with open(data_path) as data:
            str_data = data.readlines()
        test_data = str2list(str_data)
        test_data = convert_data(test_data)

    except Exception as e:
        print(e)
        exit(1)
        
    ex02.test(test_data)