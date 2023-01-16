from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request

def filecominer():
        path = os.getcwd()
        os.chdir(path)
        finallist = []

        def convert_json_to_text():
            def read_json_file(file_path):
                f = open(file_path)
                data = json.load(f)
                for i in data:
                    with open("knockpy.txt", 'a') as f:
                        if i != '_meta':
                            f.write(i + '\n')
                        f.close()

            for file in os.listdir():
                # Check whether file is in text format or not
                if file.endswith(".json"):
                    file_path = f"{path}/{file}"
                    read_json_file(file_path)

        def combiner():
            # will read one file and it will return the value of that
            def read_text_file(file_path):
                with open(file_path, 'r') as f:
                    return f.read()

            # it will write by reciving value from read_text_file() function.
            def write():
                with open('final.txt', 'a') as f:
                    f.write(read_text_file(file_path))
                    f.close()

            # iterate through all file
            for file in os.listdir():
                # Check whether file is in text format or not
                if file.endswith(".txt"):
                    file_path = f"{path}/{file}"

                    # call read text file function
                    read_text_file(file_path)
                    write()

            # will remove the duplicat value form final.txt file.
            def removeduplicate():
                with open(path + r'/final.txt', 'r') as f:
                    data = f.read().split('\n')
                    for i in data:
                        finallist.append(i)
                    setfinal = set(finallist)
                    listfinal = list(setfinal)
                    with open('without_duplicat.txt', 'a') as f:
                        for line in listfinal:
                            if line != "":
                                f.write(line + '\n')
                        f.close()

            removeduplicate()
            # will remove the final file which is useless.
            os.remove(path + r'/final.txt')
            # os.remove(path + r'\knockpy.txt')

        convert_json_to_text()
        combiner()
