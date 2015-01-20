import time
import re
import string
import random
from hashlib import sha1
import sqlite3
import sys
import shutil


datain = []
notedata = []
carddata = []
collectiondata = {}

filein = '../output/Breeds.txt'
database = '../output/collection.anki2'

#anki uses time in ms for ID
t = int(time.time()*1000)


def main():
    openFile(filein)
    genNote()
    genCard()
    genCollection()
    mediadata = genMedia()

    writeMediaData('../output/media', mediadata)
    writeSQLData()

def openFile(f):
    with open(f, 'r') as filein:
        for i, line in enumerate(filein):
            datain.append([])
            #file is tab delimited; separating data according
            el = re.split(r'\t+', line.rstrip('\n'))
            #each element it placed into a dictionary (key: name, val: imgsrc)
            datain[i].extend([el[0], el[1]])

def writeFile(f, data):
    with open(f, 'w') as fileout:
        fileout.write(data)

def genNoteID():
        return t + 1

def genGUID():
    s = string; table = s.ascii_letters + s.digits + "!#$%&()*+,-./:;<=>?@[]^_`{|}~"

    #anki using a randomised int to generate the guid str
    buf = ""
    num = random.randint(0, 2**64-1)
    while num:
        num, j = divmod(num, len(table))
        buf = table[j] + buf
    return buf

def genModified():
    return t

def genModelID():
    return t - 2000
        
def genNoteFull(index):
    #anki recognises this character as the divide between the front and back of a cardchr(0x1f)
    edge = chr(0x1f)
    front = "<div><img src=\"{}\" /></div>".format(datain[index][0].replace(' ', '-'))
    return front + edge + datain[index][0]

def genNoteSummary(index):
    return datain[index][0]

def genChecksum(index):
    """ This function consistents of several functions taken from anki git"""
    reStyle = re.compile("(?s)<style.*?>.*?</style>")
    reScript = re.compile("(?s)<script.*?>.*?</script>")
    reTag = re.compile("<.*?>")
    reEnts = re.compile("&#?\w+;")
    reMedia = re.compile("<img[^>]+src=[\"']?([^\"'>]+)[\"']?[^>]*>")

    s = reMedia.sub(" \\1 ", datain[index][0])
    s = reStyle.sub("", s)
    s = reScript.sub("", s)
    s = reTag.sub("", s)
    
    
    # entitydefs defines nbsp as \xa0 instead of a standard space, so we
    # replace it first
    s = s.replace("&nbsp;", " ")
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    s = reEnts.sub(fixup, s)

    s = s.encode("utf-8")
  
    if isinstance(s, unicode):
        s = s.encode("utf-8")
    s = sha1(s).hexdigest()
    s = s[:8]

    return int(s, 16)

def genCardID():
        return t

def getNoteID(index):
    return notedata[index]['id']

def genDeckID():
    return t - 1000

def genDue(index):
    return 1200 + index

def genCreated():
    return t - 5000

def genSchema():
    return t -500

def genConf():
    conf = "{\"nextPos\": 1, \"estTimes\": true, \"activeDecks\": [1], \"sortType\": \"noteFld\", \"timeLim\": 0, \"sortBackwards\": false, \"addToCur\": true, \"curDeck\": 1, \"newBury\": true, \"newSpread\": 0, \"dueCounts\": true, \"curModel\": \"" + str(genModelID()) + "\", \"collapseTime\": 1200}"
    return conf

def genModels():
    modelID = "{\"" + str(genModelID()) + "\": {\"vers\": [], \"name\": \"Basic-d315e\", \"tags\": [], \"did\": " + str(genDeckID()) + ", \"usn\": 330, \"req\": [[0, \"all\", [0]]], \"flds\": [{\"name\": \"Front\", \"media\": [], \"sticky\": false, \"rtl\": false, \"ord\": 0, \"font\": \"Arial\", \"size\": 20}, {\"name\": \"Back\", \"media\": [], \"sticky\": false, \"rtl\": false, \"ord\": 1, \"font\": \"Arial\", \"size\": 20}], \"sortf\": 0, \"latexPre\": \"\\\\documentclass[12pt]{article}\\n\\\\special{papersize=3in,5in}\\n\\\\usepackage{amssymb,amsmath}\\n\\\\pagestyle{empty}\\n\\\\setlength{\\\\parindent}{0in}\\n\\\\begin{document}\\n\", \"tmpls\": [{\"name\": \"Card 1\", \"qfmt\": \"{{Front}}\", \"did\": null, \"bafmt\": \"\", \"afmt\": \"{{FrontSide}}\\n\\n<hr id=answer>\\n\\n{{Back}}\", \"ord\": 0, \"bqfmt\": \"\"}], \"latexPost\": \"\\\\end{document}\", \"type\": 0, \"id\": \"" + str(genModelID()) + "\", \"css\": \".card {\\n font-family: arial;\\n font-size: 20px;\\n text-align: center;\\n color: black;\\n background-color: white;\\n}\\n\", \"mod\": " + str(genModified()) + "}}"
    return modelID

def genDecks():
    decks = "{\"" + str(genDeckID()) + "\": {\"desc\": \"Common dog breeds.\", \"name\": \"Dog Breeds\", \"extendRev\": 50, \"usn\": -1, \"collapsed\": true, \"newToday\": [338, 0], \"timeToday\": [338, 0], \"dyn\": 0, \"extendNew\": 10, \"conf\": 1, \"revToday\": [338, 0], \"lrnToday\": [338, 0], \"id\": " + str(genDeckID()) + ", \"mod\": " + str(genModified()) + "}}"
    return decks

def genConfd():
    confd = "{\"1\": {\"name\": \"Default\", \"replayq\": true, \"lapse\": {\"leechFails\": 8, \"minInt\": 1, \"delays\": [10], \"leechAction\": 0, \"mult\": 0}, \"rev\": {\"perDay\": 100, \"fuzz\": 0.05, \"ivlFct\": 1, \"maxIvl\": 36500, \"ease4\": 1.3, \"bury\": true, \"minSpace\": 1}, \"timer\": 0, \"maxTaken\": 60, \"usn\": 0, \"new\": {\"perDay\": 20, \"delays\": [1, 10], \"separate\": true, \"ints\": [1, 4, 7], \"initialFactor\": 2500, \"bury\": true, \"order\": 1}, \"mod\": 0, \"id\": 1, \"autoplay\": true}}"
    return confd
    
def genNote():
    for i in range(len(datain)):
        notedata.append({})
        notedata[i]['id'] = genNoteID() + i
        notedata[i]['guid'] = genGUID()
        notedata[i]['mid'] = genModelID()
        notedata[i]['mod'] = genModified()
        notedata[i]['usn'] = -1
        notedata[i]['tags'] = ''
        notedata[i]['flds'] = genNoteFull(i)
        notedata[i]['sfld'] = genNoteSummary(i)
        notedata[i]['csum'] = genChecksum(i)
        notedata[i]['flags'] = ''
        notedata[i]['data'] = ''


def genCard():
    for i in range(len(datain)):
        carddata.append({})
        carddata[i]['id'] = genCardID() + i
        carddata[i]['nid'] = getNoteID(i)
        carddata[i]['did'] = genDeckID()
        carddata[i]['ord'] = 0
        carddata[i]['mod'] = genModified()
        carddata[i]['usn'] = -1
        carddata[i]['type'] = 0
        carddata[i]['queue'] = 0
        carddata[i]['due'] = genDue(i)
        carddata[i]['ivl'] = 0
        carddata[i]['factor'] = 2500
        carddata[i]['reps'] = 0
        carddata[i]['lapses'] = 0
        carddata[i]['left'] = 2002
        carddata[i]['odue'] = 0
        carddata[i]['odid'] = 0
        carddata[i]['flags'] = 0
        carddata[i]['data'] = 0


def genCollection():    
        collectiondata['id'] = 1
        collectiondata['crt'] = genCreated()
        collectiondata['mod'] = genModified()
        collectiondata['scm'] = genSchema()
        collectiondata['ver'] = 11
        collectiondata['dty'] = 0
        collectiondata['usn'] = 0
        collectiondata['ls'] = 0
        collectiondata['conf'] = genConf()
        collectiondata['models'] = genModels()
        collectiondata['decks'] = genDecks()
        collectiondata['dconf'] = genConfd()
        collectiondata['tags'] = "{}"

def genMedia():
    mediadata = '{'
    for i in range(len(datain)):
        if i is 0:
            mediadata += '\"' + str(i) + '\": '
            mediadata += '\"' + datain[i][0].replace(' ', '-') + '\"'
        else:
            mediadata += ', \"' + str(i) + '\": '
            mediadata += '\"' + datain[i][0].replace(' ', '-') + '\"'
    mediadata += '}'

    return mediadata

def writeMediaData(fw, data):
    writeFile(fw, data)

def writeSQLData():
    shutil.copyfile("../other/emptysqlite.anki2", "../output/collection.anki2")
    
    con = sqlite3.connect(database)

    with con:

        cur = con.cursor()
        
        for i in range(len(notedata)):
            cur.execute("INSERT INTO notes(id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (notedata[i]['id'], notedata[i]['guid'], notedata[i]['mid'], notedata[i]['mod'], notedata[i]['usn'], notedata[i]['tags'], notedata[i]['flds'], notedata[i]['sfld'], notedata[i]['csum'], notedata[i]['flags'], notedata[i]['data']))
            
        for i in range(len(carddata)):
            cur.execute("INSERT INTO cards(id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, reps, lapses, left, odue, odid, flags, data) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (carddata[i]['id'], carddata[i]['nid'], carddata[i]['did'], carddata[i]['ord'], carddata[i]['mod'], carddata[i]['usn'], carddata[i]['type'], carddata[i]['queue'], carddata[i]['due'], carddata[i]['ivl'], carddata[i]['factor'], carddata[i]['reps'], carddata[i]['lapses'], carddata[i]['left'], carddata[i]['odue'], carddata[i]['odid'], carddata[i]['flags'], carddata[i]['data']))
            
        cur.execute("INSERT INTO col(id, crt, mod, scm, ver, dty, usn, ls, conf, models, decks, dconf, tags) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (collectiondata['id'], collectiondata['crt'], collectiondata['mod'], collectiondata['scm'], collectiondata['ver'], collectiondata['dty'], collectiondata['usn'], collectiondata['ls'], collectiondata['conf'], collectiondata['models'], collectiondata['decks'], collectiondata['dconf'], collectiondata['tags'])) 

if __name__ == '__main__':
    main()
