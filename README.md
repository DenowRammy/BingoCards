# BingoCards
A Bingo Card generator for E3 and Nintendo Direct events

How to use:

Fill the /cards/ directory with an appropriate number of images for each cell of your bingo card. The filenames will be impriinted upon the image after its cropped and resized
Run bingo.py and it will prompt you through your options, giving you the ability to select what type of card it is, how large you want the card to be, whether you want a free space, and a name to add to the bottom of the card.
Once you've entered everything, the card will automatically generate and be saved as bingo_out.png

If you'd like to add more types of cards for different events, you need to add files to the /assets/ directory. They must have a file name akin to ${type}_logo.png and ${type}_free.png and are for the logo at the top of the card, and the optional freespace in the middle respectively.
You must then edit the presets.json file and add a new object with the key being what will be entered at the time of the command prompt, a type property with the value being what the prefix in /assets/ is, and the hexadecimal colour value the card's background should be.

Dependencies:

Requires Python Pillow, and numpy.

I have no interest in maintaining this repository, fork it as you please. I might update in the future to make it better, but it's unlikely.
