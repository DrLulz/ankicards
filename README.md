Anki Card Generator
==============

This is a very basic way to generate anki cards from a set of images and data. The following are some of anki's critical concepts key to this problem. Anki uses a SQLite data with several tables to track cards, notes, decks and collections. Anki stores card display text in a single database field and uses a special character to distinguish the card sides (chr(0x1f)). To insert images into cards, anki uses a set of html tags: ```<div><img src="image name" /></div>```.

An Anki package (.apkg) is a zip file which contains a SQLite database, set of images (named '0', '1', '2', ... , 'nth') and a file which links the images to the cards (named 'media'). This media files specifies the image number and the images name.
The specifics of this problem are hardcoded into the scripts.