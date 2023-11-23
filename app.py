import time
import multiprocessing
from item_id_finder import programIDF
from steam_price_parser import programSPP
from lis_skins_item_parser import programLSIP

if __name__ == '__main__':
    processIDF = multiprocessing.Process(target=programIDF)
    processSPP = multiprocessing.Process(target=programSPP)
    processLSIP = multiprocessing.Process(target=programLSIP)

    processIDF.start()
    processIDF.join()

    processSPP.start()
    time.sleep(2)
    processLSIP.start()

    processLSIP.join()
    processSPP.join()
