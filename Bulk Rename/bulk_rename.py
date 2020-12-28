import argparse, os
import med
from math import floor


parser = argparse.ArgumentParser(description='Mass renames files in a non standard format like Big.Mouth.S04E01.WEBRip.x264-ION10.mp4 to S04E01.mp4')




def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value \n" % value)
    return ivalue

def check_dir(dir):
    value = str(dir)
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("%s is not a valid directory path \n" % value)
    
    return value

def get_renameable_files(dir):
    files = os.listdir(dir)
    acceptable_types = ["mp4","mkv","flv","avi","wmv"]

    good_files = []

    for file in files:
        if file.split(".")[-1] in acceptable_types:
            good_files.append(file)
    return sorted(good_files)

class Rename:
    def __init__(self,new,old):
        self.new_name = new
        self.old_name = old

def generate_options(files,season):
    options = []
    for i,file in enumerate(files):
        renamed = "S"+str(season)+"E"
        
        if i+1 < 10:
            renamed += str(0)+str(i+1)+"."+file.split(".")[-1]
        else:
            renamed += str(i+1)+"."+file.split(".")[-1]
        
        options.append(Rename(renamed,file))
    return options

def similarity(str1,str2):
    distance = med.distance(str1,str2)
    if len(str1) > len(str2):
        return 1-(distance/len(str1))
    else:
        return 1 -(distance/len(str2))

def format_number(number,length = 19):
    num = str(number)
    if len(num) >= length:
        return num
    else:
        return num + "0"* (length-len(num))

def max_length_old(options):
    max_len = 0

    for i in options:
        if len(i.old_name) > max_len:
            max_len = len(i.old_name)
    return max_len 


def prompt_user(options):
    max_length = max_length_old(options)
    old_to_new_pad = floor(max_length/2) + 8  
    
    print(8*" ","Sim to Previous",old_to_new_pad*" ","Old",(8+old_to_new_pad)*" ","New",8*" ", "Number")

    for i,option in enumerate(options):
        if i > 0:
            sim = similarity(option.old_name, options[i-1].old_name)
        else:
            sim = 1.0        
        print(8*" ",format_number(sim),8*" ",option.old_name, ((2*old_to_new_pad)-len(option.old_name))*" ",option.new_name,6*" ",i+1)
    
    while True:
        action = input("Should I rename y/n: ")
        cap = action.upper()

        if cap == "Y" or cap == "YES":
            return True
        elif cap == "N" or cap == "NO":
            return False

def rename(dir,options):
    for i in options:
        print("Renaming ",dir+"/"+i.old_name, "to", dir+"/"+i.new_name)
        os.rename(dir+"/"+i.old_name, dir+"/"+i.new_name)

parser.add_argument('-season', help='the seeason that the files are going to be renamed to. Expects to be a positive integer', type=check_positive , required=True)
parser.add_argument('-dir', help='directory to rename files in', type=check_dir , required=True)
args = parser.parse_args()

season = args.season
dir = args.dir
files = get_renameable_files(dir)
options = generate_options(files,season)
if prompt_user(options):
    rename(dir,options)