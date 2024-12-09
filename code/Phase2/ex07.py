import os

current_file_path = os.path.abspath(__file__)
HTML_PATH = current_file_path.replace(os.path.join("code", "Phase2", "ex07.py"), os.path.join("source", ""))

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    return wrapper

class PageRank:
    def __init__(self, pages_detail):
        self.pages_detail = pages_detail
        self.pages_name = self.pages_detail.keys()
        self.importances = {page_name:1.0 for page_name in self.pages_name}
        self.link_nums = {page_name:sum([1 for p in self.pages_detail[page_name] if p in self.pages_detail]) for page_name in self.pages_name}

    def score_update(self):
        new_importances = {}
        for page_name in self.pages_name:
            linkScore_sum = sum(
                [self.importances[p] / self.link_nums[p] for p in self.pages_detail if page_name in self.pages_detail[p]]
            )
            new_importances[page_name] = 0.15 + 0.85 * linkScore_sum
        self.importances = new_importances

    def score(self, k:int=20):
        for _ in range(k):
            self.score_update()

    def get_score(self, normalization:bool=False):
        if (normalization):
            max_score = max(self.importances.values())
            return {page:score/max_score for page,score in self.importances.items()}
        else:
            return self.importances

    
@error_handler
def unpack(d_path:str=HTML_PATH)->dict:
    files_detail = {}
    
    files = os.listdir(d_path)
    for file in files:
        with open(d_path+file, "r") as f:
            files_detail[file] = f.read().split()
            
    return files_detail


def main():
    p = PageRank(unpack())
    p.score()
    print(p.get_score(normalization=True))
        
if (__name__ == "__main__"):
    main()