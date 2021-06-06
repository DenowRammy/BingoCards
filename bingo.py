from os import listdir
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import random
import numpy as np
import math

bingo_path = "bingo.png";

h_w = 139*2

def read_image(path):
	try:
		image = Image.open(path)
		return image;
	except Exception as e:
		print(e)

def resize_image(im):
	width, height = im.size;

	print("height%s"%height)
	print("width%s"%width)
	if (height < width):
		width = int(1.0* h_w / height * width)
		height = h_w
	else:
		height = int(1.0* h_w / width * height)
		width = h_w

	print("height%s"%height)
	print("width%s"%width)
	bg = Image.new("RGB",(h_w,h_w),"#DDDDDD")
	bg.paste( im.resize((width, height),Image.LANCZOS) , (math.floor(h_w/2 - width/2), math.floor(h_w/2 - height/2)))
	return bg

def paste_image(src, paste, x, y):
	im = Image.open("cards/" + paste)

	im = resize_image(im)

	draw = ImageDraw.Draw(im)
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("LemonMilk.otf", 30)
	#draw.text((0, 0),paste,(0,0,0),font=font)
	shadowcolor = "#000000"
	wd = 14

	baseline = margin = offset = 1
    
	for line in textwrap.wrap(paste[:-4], width=wd):
		for i in range(4):
			draw.text((margin-i, offset), line, font=font, fill=shadowcolor)
			draw.text((margin+i, offset), line, font=font, fill=shadowcolor)
			draw.text((margin, offset-i), line, font=font, fill=shadowcolor)
			draw.text((margin, offset+i), line, font=font, fill=shadowcolor)
		offset += font.getsize(line)[1]
	margin = offset = baseline
	for line in textwrap.wrap(paste[:-4], width=wd):
		draw.text((margin, offset), line, font=font, fill="#FFFFFF")
		offset += font.getsize(line)[1]
	src.paste(im, ((21+163*y)*2,(274+163*x)*2))

image = read_image(bingo_path)

cards = listdir("cards/")
random.shuffle(cards)

x=0
for i in range(5):
	for j in range(5):
		if not(i == 2 and j == 2):
			print(x)
			paste_image(image,cards[x],i,j)
			x = x + 1

image.save("bingo_out.png")