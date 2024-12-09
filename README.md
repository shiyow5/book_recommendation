[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/t57ZVucK)

# Team SUS  
member:
- s1300221
- s1300097
- s1300215

## Phase1  
evals(ユーザごとの書籍評価データ)={user_id: list of evaluetion}  
例) `{1: [2, -1, 1, -1, 0], 2: [3, 1, -1, 4, 5]}`  
### Ex1　類似ユーザの検出
#### 担当：s1300215
#### 関数定義
```python
def vector_similarity(vec1:list, vec2:list)->int:
  return similarity
```
引数：２つのベクトル  
返り値：類似度＝1/(距離+1)  
```python
def similarity_list(target:int, evals:dict, sort:bool)->(dict or list):  
  return similaritys
```
引数：ターゲットユーザ、ユーザごとの書籍評価データ、ソートの可否  
返り値：ユーザ類似度(辞書型またはリスト型)  

### Ex2　アイテムの推薦
#### 担当：s1300221
#### 関数定義
```python
def recommendation(target:int, evals:dict, sort:bool)->(dict or list):
  return recommendations
```
引数：ターゲットユーザ、ユーザごとの書籍評価データ、ソートの可否  
返り値：targetに対する推薦書籍(辞書型またはリスト型)  

### Ex3　システムの効率化
b_history(ユーザたちの評価履歴)=[[user_id, book, point]]  
例) `[[1, 1, 2], [2, 3, -1]]`  
#### 担当：s1300215
#### 関数定義
```python
def convert_data(b_history:list)->dict:
  return converted
```
引数：ユーザたちの評価履歴  
返り値：ユーザごとの書籍評価データ(辞書型)  

### Ex4　インターフェースの実装 Part. 1
commands(コマンドセット)=[command, i, j, v]  
例) `['rec', 2]`  
#### 担当：s1300097
#### 関数定義：
```python
def run_command(evals:dict, commands:list)->None:
  return
```
引数：ユーザごとの書籍評価データ、コマンドセット  
返り値：なし  

## Phase2  
### Ex5　友達の検出
#### 担当：s1300215
#### アルゴリズム
UnionFindでの繋がり検知
#### クラス定義
```python
class UnionFind:
  def __init__(self, size):
  def find(self, p):
  def union(self, p, q):
  def connected(self, p, q):
```
### Ex6　ＳＮＳ情報の利用
特になし。
#### 担当：s1300097

### Ex7　書籍の重要度
importances(ページごとの重要度)={file_name:importance}  
例) `{'data.html': 1.58, 'sort.html': 0.66}`  
  
files_detail(ファイルごとの内容一覧)={file_name:[words]}  
例) `{'data.html': ['list', 'array', 'queue', 'stack', 'array', 'graph.html']}`  

#### 担当：s1300221
#### アルゴリズム
PageRankでの重要度計算  
#### 関数定義
```python
def unpack(d_path:str)->dict:
  return files_detail
```
引数：ディレクトリsourceのパス  
返り値：ファイルごとの内容一覧(辞書型)  
```python
def PageRank(files_detail:dict)->dict:
  return importances
```
引数：ファイルごとの内容一覧  
返り値：ページごとの重要度(辞書型)  

### Ex8　検索エンジンの実装
relations(ワードの関連度一覧)={file_name:relation}  
例) `{'data.html': 0.67, 'sort.html':0.00}`  

#### 担当：s1300097
#### 関数定義
```python
def rel_word(files_detail:dict, keyword:str)->dict:
  return relations
```
引数：ファイルごとの内容一覧、検索ワード  
返り値：ワードの関連度一覧(辞書型)  

## Phase3  
### Ex9　データベースによる永続化
### Ex10　ユーザインタフェースの実装
### Ex11　推薦機能・検索エンジンの強化
