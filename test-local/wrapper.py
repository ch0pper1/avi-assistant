# import the Code Engine function: func/__main__.py
from func.__main__ import main
import sys, json

if __name__ == "__main__":
    # open file, read JSON config
    with open(str(sys.argv[1])) as confFile:
        params=json.load(confFile)
    # invoke the CE function and print the result
    print(main(params))
