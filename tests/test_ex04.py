import random
import sys
import os
from code.Phase1 import ex02, ex04

class Testar_ex04():
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex04.py'), os.path.join('inputs', 'ex04_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex04.py'), os.path.join('outputs', 'ex04_test.txt'))

        self.testData = [["rec", i] for i in range(1, 7)]
        self.testData += [["eval", 1, 3, 3.7]]
        self.command_line = []
        self.dict = {1: [2.5, 5.0, -1.0, 3.0, -1.0, -1.0],
                    2: [5.0, 3.0, 3.0, -1.0, 2.0, 3.0],
                    3: [2.8, 4.5, 3.0, 2.8, 1.0, 3.6],
                    4: [1.0, 4.0, -1.0, -1.0, 2.0, 3.0],
                    5: [1.0, 1.0, 1.0, 1.0, 1.0, -1.0]}

    def generate_data(self, seed:int=0):
        random.seed(seed)
        command = ["rec", "rec", "eval"]
        com = random.choice(command)
        i = random.randint(1, 5)
        testCase = [com, i]
        if com == "eval":
            j = random.randint(1, 6)
            v = round(random.uniform(0, 5), 1)
            testCase += [j, v]
        elif random.choice([0, 1]):
            j = random.randint(1, 6)
            testCase += [j]

        self.testData.append(testCase)

    def read_testData(self):
        try:
            with open(self.INPUT_PATH, 'r') as data:
                str_data = data.readlines()

        except Exception as e:
            print(e)
            exit(1)

        k = 0
        while True:
            if (str_data[k]=='EOF'):
                break
            match len(str_data[k].split()):
                case 1:
                    command = str_data[k]
                case 2:
                    rec, i = str_data[k].split()
                    command = [rec, i]
                case 3:
                    rec, i, j = str_data[k].split()
                    command = [rec, i, j]
                case 4:
                    rec, i, j, v = str_data[k].split()
                    command = [rec, i, j, v]
            self.command_line.append(command)
            k += 1
        return str_data

    def save_testData(self):
        try:
            with open(self.INPUT_PATH, 'w') as data:
                for testCase in self.testData:
                    data.writelines(' '.join(map(str, testCase)) + '\n')
                
                data.writelines('q\nEOF')

        except Exception as e:
            print(e)
            exit(1)

        self.read_testData()

    def do_test(self):
        print("Ex04 Testing...")
        self.save_testData()
        f = open(self.OUTPUT_PATH, 'w')
        sys.stdout = f

        for i, commands in enumerate(self.command_line):
            print(f"\n<test case {i}>")
            if(commands[0] == "eval"):
                for d in self.dict:
                    print(self.dict[d])
                print()

            try:
                ex04.run_command(self.dict, commands)
            except Exception as e:
                print(e)

            if(commands[0] == "eval"):
                for d in self.dict:
                    print(self.dict[d])

        sys.stdout = sys.__stdout__
        f.close()
        print("Complete!")

def test_ex04():
    t = Testar_ex04()
    for i in range(100):
        t.generate_data(i * 123456)
    t.do_test()

if __name__ == "__main__":
    test_ex04()