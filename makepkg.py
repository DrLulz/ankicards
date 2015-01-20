import zipfile
import os

with zipfile.ZipFile('../output/dogbreeds.apkg', 'w') as zFile:
    for filename in os.listdir("../images/"):
        zFile.write("../images/" + filename, filename)
    zFile.write("../output/media", 'media')
    zFile.write("../output/collection.anki2", 'collection.anki2')
