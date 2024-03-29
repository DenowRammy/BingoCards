import textwrap, random, numpy as np, math, os
from PIL import Image, ImageFont, ImageDraw
from time import perf_counter
from os import listdir

#variables for layout
margins_size, cells_size, border_size = (33, 288, 10)
highlight_opacity, shadow_opacity, celltop_opacity, cellbottom_opacity = (170, 128, 140, 80)
letters_per_line, name_line_size = (13, 150)

presets = {
    "direct":{
        "type":"direct",
        "color":"#e41318ff",
        "namecolor":(255,255,255)
    },
    "e3":{
        "type":"e3",
        "color":"#353a4aff",
        "namecolor":(255,255,255)
    },
    "stateofplay":{
        "type":"stateofplay",
        "color":"#006fcdff",
        "namecolor":(255,255,255)
    },
    "tga":{
        "type":"tga",
        "color":"#eeeeeeff",
        "namecolor":(60,60,60)
    }
}

if True:
    while True:
        print("What type of card are you doing? Choices are " + ', '.join(presets.keys()))
        response = input()
        type = presets[response]["type"]
        color = presets[response]["color"]
        namecolor = presets[response]["namecolor"]
        if response not in presets:
            print("Please try again")
            continue
        break

    free = True
    print("Type 'no' if you would like to exclude the free space")
    if input() == "no":
        free = False

    print("How many columns and rows should there be?")
    size = int(input())

    print("What is the name on the card?")
    name = input()
else:
    response = "e3"
    type = presets[response]["type"]
    color = presets[response]["color"]
    namecolor = presets[response]["namecolor"]
    free = True
    size = 5
    name = "ram"

print("Card printing imminently...")


#functions
def make_shadow_box(width,height,toplight,bottomlight):
    border_edges_image = Image.new("RGBA", (width, height), "#0000")
    draw = ImageDraw.Draw(border_edges_image)
    draw.polygon([
        (0,0),(border_size,border_size),(border_size,height-border_size),(0,height)
    ],fill=toplight)
    draw.polygon([
        (0,0),(border_size,border_size),(width-border_size,border_size),(width,0)
    ],fill=toplight)
    draw.polygon([
        (width,0),(width,height),(width-border_size,height-border_size),(width-border_size,border_size)
    ],fill=bottomlight)
    draw.polygon([
        (0,height),(border_size,height-border_size),(width-border_size,height-border_size),(width,height)
    ],fill=bottomlight)
    return border_edges_image

t_start = perf_counter()

#get assets
if free:
    with Image.open("assets/" + type + "_free.png") as freespace:
        freespace.convert("RGBA")
with Image.open("assets/"+type+"_logo.png") as logo:
    logo.convert("RGBA")

print("Checkpoint 1", perf_counter()-t_start)
t_start = perf_counter()

#calculate and create background at size
width = size * (margins_size + cells_size) + margins_size
if margins_size * 2 + logo.width > width:
    width = margins_size * 2 + logo.width
image = Image.new("RGBA", (width, size * (margins_size + cells_size) + margins_size * 3 + logo.height + name_line_size), color)

#create highlighted border edges
image.alpha_composite(
    make_shadow_box(
        image.width,
        image.height,
        (255,255,255,highlight_opacity),
        (0,0,0,shadow_opacity)
    )
)

print("Checkpoint 2", perf_counter()-t_start)
t_start = perf_counter()

#draw logo
image.alpha_composite(logo,(math.floor(image.width/2 - logo.width / 2),margins_size),(0,0))

def get_card(path):
    im = Image.open("cards/" + path).convert("RGBA")

    #resize the image
    if im.width > im.height:
        box=(
            math.floor(im.width/2-im.height/2),
            0,
            math.floor(im.width/2+im.height/2),
            im.height
        )
    else:
        box=(
            0,
            math.floor(im.height/2-im.width/2),
            im.width,
            math.floor(im.height/2+im.width/2)
        )
    im = im.crop(box).resize((cells_size,cells_size))
    
    #give it a shadowbox
    im.alpha_composite(
        make_shadow_box(
            im.width,
            im.height,
            (0,0,0,celltop_opacity),
            (0,0,0,cellbottom_opacity)
        )
    )

    name = os.path.splitext(path)[0]

    #add text to the image
    font = ImageFont.truetype("LemonMilk.otf", 30)
    words = '\n'.join(textwrap.wrap(name,letters_per_line))
    draw = ImageDraw.Draw(im)
    draw.text((border_size,0),words,font=font, fill=(0,0,0))
    draw.text((border_size+2,0),words,font=font, fill=(0,0,0))
    draw.text((border_size,2),words,font=font, fill=(0,0,0))
    draw.text((border_size+2,2),words,font=font, fill=(0,0,0))
    draw.text((border_size+1,1),words,font=font, fill=(255,255,255))

    return im

#get images and crop
cards = listdir("cards/")
random.shuffle(cards)
cards_array = []
for index,value in enumerate(cards):
    if free and math.floor((size*size)/2) == index:
        cards_array.append(freespace)
    cards_array.append(get_card(value))

print("Checkpoint 3", perf_counter()-t_start)
t_start = perf_counter()

for index,value in enumerate(cards_array):
    if (index>=size*size):
        break
    
    image.paste(
        value,
        (
            math.floor(image.width / 2 - (size * cells_size + (size - 1) * margins_size)/2 + ((index % size) * cells_size + ((index % size) ) * margins_size) + cells_size/2 - value.width/2),
            math.floor(index/size) * (margins_size + cells_size) + margins_size * 2 + logo.height + math.floor(cells_size / 2 - value.height / 2)
        ),
        value
    )

print("Checkpoint 4", perf_counter()-t_start)
t_start = perf_counter()

#write name at the bottom of the card
font = ImageFont.truetype("SylexiadSansMedium-Bold.otf", 270)
draw = ImageDraw.Draw(image)
draw.text(
    (
        margins_size,
        image.height-margins_size-math.floor(name_line_size*1.25)
    ),
    name,font=font,fill=namecolor
)

print("Checkpoint 5", perf_counter()-t_start)

#size * (margins_size + cells_size) + margins_size * 2 + logo.height)
#save image
image.save("bingo_out.png")
print("Card printing complete, please read your files")
