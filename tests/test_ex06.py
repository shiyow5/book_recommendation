import random
import sys
import os
from code.Phase1.ex03 import *
from code.Phase2 import ex05
from code.Phase2 import ex06

class Testar_ex06():
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex06.py'), os.path.join('inputs', 'ex06_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex06.py'), os.path.join('outputs', 'ex06_test.txt'))
        
        # set default test case
        self.testData = [([8, 5, 28],
                          [[1, 1, 5.0], [1, 2, 2.0], [2, 4, 5.0], [3, 1, 5.0],
                           [3, 2, 2.0], [3, 3, 5.0], [3, 4, 2.0], [3, 5, 2.0],
                           [4, 1, 1.0], [4, 2, 5.0], [4, 5, 4.0], [5, 1, 2.0],
                           [5, 2, 2.0], [5, 3, 5.0], [6, 1, 4.0], [6, 2, 3.0],
                           [6, 3, 3.0], [6, 4, 3.0], [6, 5, 3.0], [7, 2, 2.0], 
                           [7, 3, 5.0], [7, 4, 2.0], [7, 5, 1.0], [8, 1, 5.0], 
                           [8, 2, 2.0], [8, 3, 1.0], [8, 4, 3.0], [8, 5, 5.0]],
                           6,
                           [[1, 2], [1, 4], [1, 6],
                            [6, 7], [7, 8], [3, 5]]
                          )]
        self.test_data = []
        self.uf = []

    def generate_data(self, seed:int=2024):
        random.seed(seed)
        N = random.randint(2, 100)
        M = random.randint(1, 100)
        E = random.randint(0, 100000)
        evals = [[random.randint(1, N), random.randint(1, M), round(random.uniform(0, 5), 1)] for _ in range(E)]
        R = random.randint(1, 100000)
        relations = [[random.randint(1, N), random.randint(1, N)]for _ in range(R)]
        testCase = ([N, M, E], evals, R, relations)
        
        self.testData.append(testCase)
        
        return testCase
    
    def save_testData(self):
        try:
            with open(self.INPUT_PATH, 'w') as data:
                for testCase in self.testData:
                    data.writelines(f"{testCase[0][0]} {testCase[0][1]} {testCase[0][2]}\n")
                    for evals in testCase[1]:
                        data.writelines(' '.join(map(str, evals)) + '\n')
                    data.writelines(f"{testCase[2]}\n")
                    for relations in testCase[3]:
                        data.writelines(' '.join(map(str, relations)) + '\n')

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
        self.test_data = []
        self.uf = []
        while True:
            if (str_data[i]=='EOF'):
                break
            
            N, _, E = map(int, str_data[i].split())
            test_data = str2list(str_data[i:i+E+1])
            self.test_data.append(convert_data(test_data))
            i += E+1
            R = int(str_data[i])
            str_data[i] = str(N) + " " + str_data[i]
            self.uf.append(ex05.str2uf(str_data[i:i+R+1]))
            i += R+2
            
        return str_data
    
    def do_test(self):
        print("Ex06 Testing...")
        self.save_testData()
        f = open(self.OUTPUT_PATH, 'w')
        sys.stdout = f
        
        for i, test_data in enumerate(self.test_data):
            print(f"\n<test case {i}>")
            for target in range(1, len(test_data)+1):
                print(f"--user {target:>3}--")
                ex06.friend_reco(test_data, self.uf[i], target, True)
        print("\nFinish")
        
        sys.stdout = sys.__stdout__
        f.close()
        print("\nComplete!")

def test_ex06():
    t = Testar_ex06()
    for i in range(5):
        t.generate_data(i * 12345)
    t.do_test()

if __name__ == "__name__":
    test_ex06()