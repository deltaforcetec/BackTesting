from io import *
import csv
import numpy

def write_to_file(file_name, mode, data):
    with open(file_name, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(data)
    #f = open(file_name, mode)
    #f.writelines(data)
    #f.close()




