import random
import sys
import os
from code.Phase2 import ex05

class Testar_ex05():
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex05.py'), os.path.join('inputs', 'ex05_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex05.py'), os.path.join('outputs', 'ex05_test.txt'))
        
        # set default test case
        self.testData = [([8, 6],
                          [[1, 2],
                           [1, 4],
                           [1, 6],
                           [6, 7],
                           [7, 8],
                           [3, 5]],
                           6,
                           [[1, 2],
                            [1, 3],
                            [1, 8],
                            [1, 5],
                            [5, 6],
                            [6, 5]]
                        )]
        self.uf = []
        self.queries = []
        
    def generate_data(self, seed:int=42):
        random.seed(seed)
        N = random.randint(2, 100000)
        R = random.randint(1, 100000)
        relations = [[random.randint(1, N), random.randint(1, N)]for _ in range(R)]
        Q = random.randint(1, 100000)
        queries = [[random.randint(1, N), random.randint(1, N)]for _ in range(Q)]
        testCase = ([N, R], relations, Q, queries)
        self.testData.append(testCase)
        
        return testCase
    
    def save_testData(self):
        try:
            with open(self.INPUT_PATH, 'w') as data:
                for testCase in self.testData:
                    data.writelines(f"{testCase[0][0]} {testCase[0][1]}\n")
                    for relations in testCase[1]:
                        data.writelines(' '.join(map(str, relations)) + '\n')
                    data.writelines(f"{testCase[2]}\n")
                    for queries in testCase[3]:
                        data.writelines(' '.join(map(str, queries)) + '\n')
                        
                    data.writelines('\n')
                data.writelines('EOF')

        except Exception as e:
            print(e)
            exit(1)
            
        self.read_testData()

    def read_testData(self):
        try:
            with open(self.INPUT_PATH, 'r') as data:
                str_data = data.readlines()

        except Exception as e:
            print(e)
            exit(1)
        
        i = 0
        self.uf = []
        self.queries = []
        while True:
            if (str_data[i]=='EOF'):
                break
            
            N, R =  map(int, str_data[i].split())
            self.uf.append(ex05.str2uf(str_data[i:i+R+1]))
            i += R+1
            Q = int(str_data[i])
            self.queries.append(ex05.str2q(str_data[i:i+Q+1]))
            i += Q+2
            
        return str_data
    
    def do_test(self):
        print("Ex05 Testing...")
        self.save_testData()
        f = open(self.OUTPUT_PATH, 'w')
        sys.stdout = f
        
        for i, queries in enumerate(self.queries):
            print(f"\n<test case {i}>", end="")
            results = ex05.judge(self.uf[i], queries)

            for i, result in enumerate(results):
                if i % 10 == 0:
                    print(f"\n{int((i+1) / 10):>5}:  ", end="")
                assert result == "yes" or result == "no"
                print(result, end="\t")
            print()
        print("\nFinish")
        
        sys.stdout = sys.__stdout__
        f.close()
        print("Complete!")

def test_ex05():
    t = Testar_ex05()
    for i in range(5):
        t.generate_data(i * 12345)
    t.do_test()

if __name__ == "__main__":
    test_ex05()