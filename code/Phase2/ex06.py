from ..Phase1.ex03 import *
from ..Phase1.ex02 import recommendation
from . import ex05

def notfriend(uf, test_data, target = 1):
    user_data = test_data.keys()
    exclude = []
    for user in user_data:
        if not uf.custom_connected(target, user):
            exclude.append(user)

    return exclude

def friend_reco(data, uf, target = 1, test = False):
    exclude = notfriend(uf, data, target)

    try:
        rec = recommendation(target, data, True, exclude)
        for r in rec:
            print(f"{r[0]:>3} {r[1]}")
    except Exception as e:
        if not test:
            print(e)

if (__name__ == '__main__'):
    file_name = 'ex06_test.txt' # テスト用のファイル名を設定
    data_path = __file__.replace('ex06.py', 'Test_data/'+file_name)
    
    try:
        with open(data_path) as data:
            str_data = data.readlines()
        test_data = str2list(str_data)
        test_data = convert_data(test_data)
        n, _, e = map(int, str_data[0].split())
        del str_data[:e+1]
        str_data[0] = str(n) + str_data[0]
        uf = ex05.str2uf(str_data)

    except Exception as e:
        print(e)
        exit(1)

    friend_reco(test_data, uf)