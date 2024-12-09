from . import ex07

def search_keyword(pack, keyword):
    # 書籍の題名も検索に影響を与えるように変更した
    scores = {name: sum(1 for word in keyword if (word.lower() in map(str.lower, html)) or (word.lower() in name.lower())) for name, html in pack.items()}
    if max(scores.values()):
        scores = {name: score / max(scores.values()) for name, score in scores.items()}
        
    return scores

def display_search(first, second, third = None, test = False):
    sorted_keys = sorted(first.keys(), key=lambda k: (first[k], second[k]), reverse=True)
    if third == None:
        third = {key: (first[key] + second[key]) for key in first.keys()}
    for i, key in enumerate(sorted_keys, 1):
        if not test:
            print(f'{first[key]:.2f} : {second[key]:.2f} : {third[key]:.2f} : {key}')
        else:
            print(f'{i:>3}   {first[key]:.2f} : {second[key]:.2f} : {third[key]:.2f} : {key}')
    return [(key, third[key]) for key in sorted_keys]

def main():
    #keyword = ['list', 'queue', 'bfs', 'list']
    keyword = input().split()
    keyword = list(set(keyword))

    pack = ex07.unpack()
    p = ex07.PageRank(pack)
    p.score()
    page = p.get_score(True)
    word = search_keyword(pack, keyword)

    display_search(word, page)
    
if (__name__ == "__main__"):
    main()