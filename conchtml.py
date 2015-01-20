import os
for filename in os.listdir("../html/"):
    with open("../html/" + filename, 'r') as infile, open("../output/concat.html", 'a') as outfile:
        outfile.write(infile.read())
