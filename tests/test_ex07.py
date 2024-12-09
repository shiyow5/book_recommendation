import random
import string
import sys
import os
from code.Phase2 import ex07

# 他のテスターと違い、複数のソースディレクトリを一斉に作るのではなく1つのソースディレクトリを更新して使っていくこととする
class Testar_ex07():
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex07.py'), os.path.join('inputs', 'test_source/'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex07.py'), os.path.join('outputs', 'ex07_test.txt'))
        
        # set default test case
        self.testData = {'algorithm.html':
'''program algorithm
sort.html
search.html data.html
data structure''',
                          'data.html':
'''list array queue
stack
array
graph.html''',
                          'graph.html':
'''list bfs dfs
queue stack 
node edge
data.html search.html''',
                          'search.html':
'''array
binary
data.html
sort.html''',
                          'sort.html':
'''sort merge
data.html array
search.html'''
                          }
        self.keywords = []
        self.urls = []
        self.save_testData()
        
        
    def generate_data(self, seed:int=0):
        random.seed(seed)
        D = random.randint(0, 100000) # document num
        ADT = random.randint(0, 1000000) # text length in all document
        DT = [random.randint(0, 10000) for _ in range(D)] # text length in document
        DT = [DT[:i] for i in range(D) if sum(DT[:i]) < ADT][-1]
        D = len(DT)
        
        document_names = list({randomstr(random.randint(2, 20)) for _ in range(D)}) # 重複を許さないようset型を挟む
        keywords = document_names + list({randomstr(random.randint(2, 20)) for _ in range(D)}) # htmlの2倍生成
        document_names = [dn + '.html' for dn in document_names]
        
        documents = {}
        for d in range(D):
            U = random.randint(0, 10) # URL num in document
            
            urls = random.sample(document_names, k=U)
                
            words = random.sample(keywords+list(urls), k=U+2*D)
            words = [words[:i] for i in range(U+2*D) if sum([len(w) for w in words[:i]]) < DT[d]][-1]
                    
            sentence = ""
            for word in words:
                if (random.choice([True, False])):
                    sentence += word+' '
                else:
                    sentence += word+'\n'
            
            documents[document_names[d]] = sentence
        
        self.testData = documents
        
        self.save_testData() # file更新も同時にしてしまう
        
        return documents
    
    def read_testData(self):
        self.testData = {}
        
        for file_name in os.listdir(self.INPUT_PATH):
            try:
                with open(self.INPUT_PATH+file_name, 'r') as data:
                    test_data = data.read()
                    
                self.testData[file_name] = test_data

            except Exception as e:
                print(e)
                exit(1)
            
        
    
    def save_testData(self):
        for file_name in os.listdir(self.INPUT_PATH):
            os.remove(os.path.join(self.INPUT_PATH, file_name))
            
        for document_name in self.testData.keys():
            try:
                with open(self.INPUT_PATH+document_name, 'w') as data:
                    data.write(self.testData[document_name])

            except Exception as e:
                print(e)
                exit(1)
            
        self.read_testData() # dict_data更新のため
    
    def do_test(self): # テストするのはあくまでそのユーザが読んでない書籍を推薦できているかどうかのみ
        print("Ex07 Testing...")
        
        f = open(self.OUTPUT_PATH, 'w')
        sys.stdout = f
        
        p = ex07.PageRank(ex07.unpack(d_path=self.INPUT_PATH))
        p.score()
        scores = p.get_score(normalization=True)
        
        for document_name in scores.keys():
            assert document_name in self.testData.keys()
            print(f"{document_name}: {scores[document_name]}")
        
        sys.stdout = sys.__stdout__
        f.close()
        
        print("Complete!")
    
        
def randomstr(n:int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    

def test_ex02():
    t=Testar_ex07()
    t.generate_data()
    t.do_test()