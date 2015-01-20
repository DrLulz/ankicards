from BeautifulSoup import BeautifulSoup
import os


#this varaible will hold all dog breeds
dataset = {}

#iterates through each element within a single resultset
def parse_string(a):
    #formatting input
    name = a['alt'].replace('-', ' ')
    imgsrc = 'http://www.purina.com.au/owning-a-dog/dog-breeds/' + a['src'] 

    #add breed and image source to variable
    dataset[name] = imgsrc
    return

#opens concatenated html file
with open("../output/concat.html", 'r') as f:
    html = f.read()

#initialises BS class
parsed_html = BeautifulSoup(html)

#returns all found instances of <ul class="breedGrid"... as several resultsets
breeds = parsed_html.findAll('ul', attrs={'class':'breedGrid'})

#iterates through each of the resultsets and for each element in a resultset, calls the parse_string function
for breed in breeds:
    data = map(parse_string, breed.findAll('img'))

#writes data to file
with open('../output/breeds.txt', 'a') as fileout:
    for idx, val in sorted(dataset.iteritems()):
        writestring = idx + "\t" + val + "\n"
        fileout.write(writestring)
