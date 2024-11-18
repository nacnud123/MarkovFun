import os
import random
import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageDraw
from PIL import ImageFont
import textwrap


def get_source(dir):
    # Finds all text located in the <src> directory
    text = ""
    files = [
        # os.path.join to keep things cross-platform friendly
        os.path.join('src', dir, name) for name in os.listdir(os.path.join('src', dir))
    ]
    for name in files:
        with open(name, encoding="utf8") as f:
            text += "\n"
            text += f.read()
    return text


def build_model(source, state_size):
    # Builds a Markvo Chain based on soruce and state_size.
    source = source.split()
    model = {}
    for i in range(state_size, len(source)):
        current_word = source[i]
        previous_words = ' '.join(source[i-state_size:i])
        if previous_words in model:
            model[previous_words].append(current_word)
        else:
            model[previous_words] = [current_word]

    return model


def generate_text(model, state_size, min_length, max_length = 50):
    # Generates text based on markov model.
    # Generates text that is at least <min_length> long and no longer than <max_length>
    def get_new_starter():
        return random.choice([s.split(' ') for s in model.keys() if s[0].isupper()])
    text = get_new_starter()

    i = state_size
    while True:
        key = ' '.join(text[i-state_size:i])
        if key not in model:
            text += get_new_starter()
            i += 1
            continue

        next_word = random.choice(model[key])
        text.append(next_word)
        i += 1
        if i > max_length or (i > min_length and text[-1][-1] == '.'):
            break
    return ' '.join(text)

def update_jerma_says():
    global image_label, img, draw
    state_size = 2
    min_length = 2
    max_length = 15
    source = get_source('Jerma')
    jerma = build_model(source, state_size)
    text = generate_text(jerma, state_size, min_length, max_length)

    img.paste(Image.open("JermaTemplate.jpg"))
    imgText = textwrap.wrap(text, 20)
    y = 125
    for x in imgText:
        draw.text((337, y), x, font=myFont, fill=(255, 0, 0))
        y += 20
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo
    draw = ImageDraw.Draw(img)


def update_garfield_says():
    global image_label, img, draw
    state_size = 2
    min_length = 2
    max_length = 5
    source = get_source('Garfield')
    garfield = build_model(source, state_size)
    text = generate_text(garfield, state_size, min_length, max_length)

    img.paste(Image.open("GarfTemplate.png"))
    imgText = textwrap.wrap(text, 20)
    y = 9
    for x in imgText:
        draw.text((107, y), x, font=myFont, fill=(255, 0, 0))
        y += 10
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo
    draw = ImageDraw.Draw(img)

def update_funny_says():
    global image_label, img, draw
    state_size = 2
    min_length = 2
    max_length = 5
    source = get_source('Funny')
    myFont = ImageFont.truetype('FreeMono.ttf', 15)
    garfield = build_model(source, state_size)
    text = generate_text(garfield, state_size, min_length, max_length)

    img.paste(Image.open("Funny.png"))
    imgText = textwrap.wrap(text, 50)
    y = 378
    for x in imgText:
        draw.text((10, y), x, font=myFont, fill=(255, 0, 0))
        y += 20
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo
    draw = ImageDraw.Draw(img)


def change_image(whichImage):
    global img, draw, font
    if whichImage == 1:
        img = Image.open("JermaTemplate.jpg")
        draw = ImageDraw.Draw(img)
        update_jerma_says()
    elif whichImage == 2:
        img = Image.open("GarfTemplate.png")
        draw = ImageDraw.Draw(img)
        update_garfield_says()
    elif whichImage == 3:
        img = Image.open("Funny.png")
        draw = ImageDraw.Draw(img)
        update_funny_says()

def save_image():
    global img
    filename = f"GeneratedImage_{random.randrange(1, 5000)}.png"
    img.save(filename)
    print(f"Image saved as {filename}")


root = tk.Tk()
img = Image.open("JermaTemplate.jpg")
draw = ImageDraw.Draw(img)
myFont = ImageFont.truetype('FreeMono.ttf', 10)

photo = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=photo)
image_label.pack()

change_to_jerma_button = tk.Button(root, text="New Jerma Says", command=lambda: change_image(1))
change_to_jerma_button.pack()

change_to_garfield_button = tk.Button(root, text="New Garfield Says", command=lambda: change_image(2))
change_to_garfield_button.pack()

change_to_funny_button = tk.Button(root, text="New Funny", command=lambda: change_image(3))
change_to_funny_button.pack()

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

root.mainloop()