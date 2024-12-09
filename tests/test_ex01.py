import random
import sys
import os

from code.Phase1 import ex01
from code.Phase1 import ex02


class TestEx01:
    def __init__(self):
        current_file_path = os.path.abspath(__file__)
        self.INPUT_PATH = current_file_path.replace(os.path.join('test_ex01.py'), os.path.join('inputs', 'ex01_test.txt'))
        self.OUTPUT_PATH = current_file_path.replace(os.path.join('test_ex01.py'), os.path.join('outputs', 'ex01_test.txt'))
        self.testData = [([5, 6],
                          [[2.5, 5.0, -1.0, 3.0, -1.0, -1.0],
                           [5.0, 3.0, 3.0, -1.0, 2.0, 3.0],
                           [2.8, 4.5, 3.0, 2.8, 1.0, 3.6],
                           [1.0, 4.0, -1.0, -1.0, 2.0, 3.0],
                           [1.0, 1.0, 1.0, 1.0, 1.0, -1.0]]
                          )]
        self.dict_datas = []

    def generate_data(self, seed: int = 0):  # ランダムなテストデータを生成するメソッド
        random.seed(seed)  # ランダムシードを設定
        N = random.randint(2, 100)  # ランダムなユーザー数を生成
        M = random.randint(1, 100)  # ランダムな評価数を生成
        evals = [[random.choice([-1.0, float(f"{random.uniform(0, 5):.1f}")]) for _ in range(M)] for _ in range(N)]  # ランダムな評価データを生成
        testCase = ([N, M], evals)  # 生成されたデータをテストケースとして格納

        self.testData.append(testCase)  # テストケースを追加

        return testCase  # 生成されたテストケースを返す

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
            if (str_data[i] == 'EOF'):
                break

            N, _ = map(int, str_data[i].split())
            self.dict_datas.append(ex02.str2dict(str_data[i:i + N + 1]))
            i += N + 2

        return str_data

    def save_testData(self):  # テストデータをファイルに保存するメソッド
        try:
            with open(self.INPUT_PATH, 'w') as data:  # 入力ファイルを開く
                for testCase in self.testData:  # テストケースごとに
                    data.writelines(f"{testCase[0][0]} {testCase[0][1]}\n")  # テストケースの情報を書き込む
                    for evals in testCase[1]:  # 各評価データごとに
                        data.writelines(' '.join(map(str, evals)) + '\n')  # 評価データを書き込む

                    data.writelines('\n')  # テストケースの区切りのために空行を追加
                data.writelines('EOF')  # ファイルの終端を示す

        except Exception as e:  # 例外が発生した場合の処理
            print(e)  # エラーメッセージを表示
            exit(1)  # プログラムを終了

        self.read_testData()  # テストデータを更新するために読み込み

    def do_test(self):  # テストを実行するメソッド
        print("Ex01 Testing...")  # テスト開始を表示
        self.save_testData()

        with open(self.OUTPUT_PATH, 'w') as f:  # 出力ファイルを開く
            sys.stdout = f  # 標準出力をファイルにリダイレクト

            for i, dict_data in enumerate(self.dict_datas):  # 各テストケースごとに
                print(f"\n<test case {i}>")  # テストケースの番号を表示
                for user in dict_data:
                    results = ex01.similarity_list(user, dict_data, True)  # テストを実行して結果を取得
                    print(f"--user {user:>3}--")
                    for j, result in enumerate(results, 1):
                        print(f"{j:>3}: {result[0]:>3} {result[1]}")

            print("\nFinish")

            sys.stdout = sys.__stdout__  # 標準出力を元に戻す

        print("Complete!")  # テスト完了を表示



def test_ex01():  # テストを実行する関数
    t = TestEx01()  # 'TestEx01' クラスのインスタンスを作成
    for i in range(10):  # 100回繰り返して
        t.generate_data(i)  # テストデータを生成
    t.do_test()  # テストを実行

if __name__ == '__main__':
    test_ex01()
