import random
import sys
import os
from code.Phase2 import ex07, ex08

class Testar_ex08():
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex08.py'), os.path.join('inputs', 'ex08_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex08.py'), os.path.join('outputs', 'ex08_test.txt'))
 
        self.testData = [ex07.unpack()]
        self.testData.append(ex07.unpack(current_file_path.replace(os.path.join('test_ex08.py'), os.path.join('inputs', 'test_source/'))))

        self.keywords = [['list', 'queue', 'bfs', 'list']]

    def generate_data(self, seed:int = 42):
        population = []
        for i in self.testData[1]:
            for data in self.testData[1][i]:
                if not data.endswith('.html'):
                    population.append(data)
        random.seed(seed)
        for i in range(20):
            self.keywords.append(random.choices(population, k=i))

    def save_testData(self):
        try:
            with open(self.INPUT_PATH, 'w') as data:
                for word in self.keywords:
                    data.writelines(' '.join(map(str, word)) + '\n\n')
                data.writelines('EOF')
        except Exception as e:
            print(e)
            exit(1)

    def do_test(self):
        print("Ex08 Testing...")
        self.save_testData()

        f = open(self.OUTPUT_PATH, 'w')
        sys.stdout = f

        for i, test_word in enumerate(self.keywords):
            print(f"\n<test case {i}>")
            if i != 0:
                testData = self.testData[1]
            else:
                testData = self.testData[0]
            p = ex07.PageRank(testData)
            p.score()
            page = p.get_score(True)
            word = ex08.search_keyword(testData, test_word)
            ex08.display_search(word, page, test=True)
        
        print("\nFinish")
        sys.stdout = sys.__stdout__
        f.close()
        
        print("Complete!")

def test_ex08():
    t = Testar_ex08()
    t.generate_data()
    t.do_test()

if __name__ == "__main__":
    test_ex08()