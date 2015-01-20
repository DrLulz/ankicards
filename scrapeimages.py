import urllib
import re

datain = []
f = "../output/Breeds.txt"
base_url = "http://urina.com.au/owning-a-dog/dog-breeds/"

def main():
    openFile(f)
    scrapeImages()

def openFile(f):
    with open(f, 'r') as filein:
        for i, line in enumerate(filein):
            datain.append([])
            #file is tab delimited; separating data according
            el = re.split(r'\t+', line.rstrip('\n'))
            #each element it placed into a dictionary (key: name, val: imgsrc)
            datain[i].extend([el[0], el[1]])

def scrapeImages():
    num = len(datain)
    for idx, el in enumerate(datain):
        print "Starting " + str(idx + 1) + " of " + str(num) + "..."
        urllib.urlretrieve(el[1], "../images/" + str(idx))
        print "Finished " + str(idx + 1) + " of " + str(num)
        

if __name__ == '__main__':
    main()
