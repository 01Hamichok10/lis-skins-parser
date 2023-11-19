import multiprocessing
from lis_skins_item_parser import programLSIP
from steam_price_parser import programSPP

if __name__ == '__main__':
    processSPP = multiprocessing.Process(target=programSPP)
    processLSIP = multiprocessing.Process(target=programLSIP)

    processSPP.start()
    processLSIP.start()

    print("Начата работка,  мяу")

    end = False
    while end == False:
        print("Введите 'end' для завершения работы:")
        if input() == "end":
            end = True

    processSPP.terminate()
    processLSIP.terminate()

    processSPP.join()
    processLSIP.join()