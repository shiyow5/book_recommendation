
import sys
import random
import os


from code.Phase1 import ex02, ex03


class Testar_ex03:

    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex03.py'), os.path.join('inputs', 'ex03_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex03.py'), os.path.join('outputs', 'ex03_test.txt'))

        self.testData = [(
            [5, 6, 23],
            [[1, 1, 2.5],
            [1, 2, 5.0],
            [1, 4, 3.0],
            [2, 1, 5.0],
            [2, 2, 3.0],
            [2, 3, 3.0],
            [2, 5, 2.0],
            [2, 6, 3.0],
            [3, 1, 2.8],
            [3, 2, 4.5],
            [3, 3, 3.0],
            [3, 4, 2.8],
            [3, 5, 1.0],
            [3, 6, 3.6],
            [4, 1, 1.0],
            [4, 2, 4.0],
            [4, 5, 2.0],
            [4, 6, 3.0],
            [5, 1, 1.0],
            [5, 2, 1.0],
            [5, 3, 1.0],
            [5, 4, 1.0],
            [5, 5, 1.0]]
        )]
        self.dict_datas = []

    def generate_data(self, case_num):
        random.seed(case_num)
        N = random.randint(2, 1000)
        M = random.randint(1, 1000)
        E = random.randint(1, 100000)

        evals = [[random.randint(1, N), random.randint(1, M), random.randint(1, E)] for _ in range(E)]
        testCase = ([N, M, E], evals)
        self.testData.append(testCase)

    def read_testData(self):
        try:
            with open(self.INPUT_PATH, 'r') as data:
                str_data = data.readlines()
        except Exception as e:
            print(e)
            exit(1)

        i = 0
        while i < len(str_data):
            if str_data[i].strip() == 'EOF':
                break
            _, _, e = map(int, str_data[i].strip().split())
            data = ex03.str2list(str_data[i:i+e+1])
            self.dict_datas.append(ex03.convert_data(data))
            i += e+2

    def save_testData(self):
        try:
            with open(self.INPUT_PATH, 'w') as data:
                for testCase in self.testData:
                    data.writelines(f"{testCase[0][0]} {testCase[0][1]} {testCase[0][2]}\n")
                    for eval in testCase[1]:
                        data.writelines(' '.join(map(str, eval)) + '\n')
                    data.writelines('\n')
                data.writelines('EOF\n')
                
        except Exception as e:
            print(e)
            exit(1)

        self.read_testData()

    def do_test(self):
        print("Ex03 Testing...")
        self.save_testData()
        original_stdout = sys.stdout
        try:
            with open(self.OUTPUT_PATH, 'w') as f:
                sys.stdout = f
                for i, data in enumerate(self.dict_datas):
                    print(f"\n<test case {i}>")
                    ex02.test(data)
                print("\nFinish")
        finally:
            sys.stdout = original_stdout
            f.close()
            print("Complete!")

def test_ex03():
    t = Testar_ex03()
    for i in range(5):
        t.generate_data(i * 12345)
    t.do_test()

if __name__ == "__main__":
    test_ex03()


