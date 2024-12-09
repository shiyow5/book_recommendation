from .ex02 import recommendation
from .ex03 import *
def run_command(evals:dict, commands:list)->None:
    N = len(evals.keys())
    M = len(evals.values())
    
    match commands[0]:
        case "rec":
            if int(commands[1]) > N:
                print("User not found.")

            elif len(commands) == 2:                                        
                target = int(commands[1])
                recommendations = recommendation(target, evals, True)
                #output
                for rec in recommendations:
                    print(rec[0], rec[1])
            
            elif len(commands) == 3:
                target = int(commands[1])
                order = int(commands[2])
                recommendations = recommendation(target, evals, True)
                #output
                if order <= len(recommendations):
                    print(recommendations[order-1][0], recommendations[order-1][1])
                else:
                    print("User not found.")
            
            else:
                print("Command input error!")


        case "eval":
            if len(commands) != 4:
                print("Command input error!")

            elif int(commands[1]) > N or int(commands[2]) > M+1:
                print("User or Book not found.")

            elif float(commands[3]) < 0 or 5 < float(commands[3]):
                print("Input error!")         

            else:                 
                evals[int(commands[1])][int(commands[2])-1] = float(commands[3])

        case "q" | "exit":
            raise Exception("Exiting by command.")

        case _:
            print("Command input error!")
    
    return

def pre_input(evals):
    while(True):
        try:
            print("supported command: rec i, rec i j, eval i j v, q(exit)")
            run_command(evals, input().split())
        except Exception as e:
            print(e)
            break

if (__name__ == '__main__'):
    file_name = 'ex03_test.txt' # テスト用のファイル名を設定
    data_path = __file__.replace('ex04.py', 'Test_data/'+file_name)
    
    with open(data_path) as data:
        str_data = data.readlines()
    test_data = str2list(str_data)
    evals = convert_data(test_data)
    pre_input(evals)