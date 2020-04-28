import sys
import inspect
from importlib import import_module
from .simulation.algorithm import Algorithm

argc = len(sys.argv)

stat = False
algo_name = ""
times = 1

try:
    if argc == 2:
        algo_name = sys.argv[1]
    elif argc == 3:
        try:
            if sys.argv[1].index("--") == 0:
                stat = True
                algo_name = sys.argv[2]
            else: raise 1
        except ValueError:
            times = int(sys.argv[2])
            algo_name = sys.argv[1]
    elif argc == 4:
        if sys.argv[1].index("--") == 0:
            stat = True
            algo_name = sys.argv[2]
            times = int(sys.argv[3])
    else: raise 1
except:
    print("Usage: [ --stat ] algorithm [ times ]")
    exit()
    
imported_module = import_module(".simulation.{}".format(algo_name), package=__package__)

for i in dir(imported_module):
    attribute = getattr(imported_module, i)

    if inspect.isclass(attribute) and issubclass(attribute, Algorithm) and attribute != Algorithm:
        scoreTotal = 0
        for i in range(times):
            score = attribute().simulate()
            scoreTotal += score
            if not stat:
                print(score)

        if stat:
            print("Mean: {}".format(scoreTotal / times))
        
