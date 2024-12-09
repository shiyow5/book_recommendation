import random
import sys
import os
from code.Phase1 import ex02

class Testar_ex02():
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex02.py'), os.path.join('inputs', 'ex02_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex02.py'), os.path.join('outputs', 'ex02_test.txt'))
        
        # set default test case
        self.testData = [([5, 6],
                          [[2.5, 5.0, -1.0, 3.0, -1.0, -1.0],
                           [5.0, 3.0, 3.0, -1.0, 2.0, 3.0],
                           [2.8, 4.5, 3.0, 2.8, 1.0, 3.6],
                           [1.0, 4.0, -1.0, -1.0, 2.0, 3.0],
                           [1.0, 1.0, 1.0, 1.0, 1.0, -1.0]]
                          )]
        self.dict_datas = []
        self.save_testData()
        
        
    def generate_data(self, seed:int=0):
        random.seed(seed)
        N = random.randint(2, 100)
        M = random.randint(1, 100)
        evals = [[random.choice([-1.0, float(f"{random.uniform(0, 5):.1f}")]) for _ in range(M)] for _ in range(N)]
        testCase = ([N, M], evals)
        
        self.testData.append(testCase)
        
        self.save_testData() # file更新も同時にしてしまう
        
        return testCase
    
    def read_testData(self):
        try:
            with open(self.INPUT_PATH, 'r') as data:
                str_data = data.readlines()

        except Exception as e:
            print(e)
            exit(1)
        
        self.dict_datas = []
        i = 0
        while True:
            if (str_data[i]=='EOF'):
                break
            
            N, _ =  map(int, str_data[i].split())
            self.dict_datas.append(ex02.str2dict(str_data[i:i+N+1]))
            i += N+2
            
        return str_data
    
    def save_testData(self):
        try:
            with open(self.INPUT_PATH, 'w') as data:
                for testCase in self.testData:
                    data.writelines(f"{testCase[0][0]} {testCase[0][1]}\n")
                    for evals in testCase[1]:
                        data.writelines(' '.join(map(str, evals)) + '\n')
                        
                    data.writelines('\n')
                data.writelines('EOF')

        except Exception as e:
            print(e)
            exit(1)
            
        self.read_testData() # dict_data更新のため
    
    def do_test(self): # テストするのはあくまでそのユーザが読んでない書籍を推薦できているかどうかのみ
        print("Ex02 Testing...")
        
        f = open(self.OUTPUT_PATH, 'w')
        sys.stdout = f
        
        for i, dict_data in enumerate(self.dict_datas):
            print(f"\n<test case {i}>")
            results = ex02.test(dict_data)
            
            for uid in results.keys():
                for bid in range(1, len(dict_data[uid])+1):
                    if (dict_data[uid][bid-1] == -1.0):
                        assert bid in [result[0] for result in results[uid]]
        
        sys.stdout = sys.__stdout__
        f.close()
        
        print("Complete!")
    

def test_ex02():
    t = Testar_ex02()
    for i in range(100):
        t.generate_data(i)
    t.do_test()
