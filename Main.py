# Duncan Armstrong - 11/9/24 - Markov Chain Script
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
        os.path.join('src', dir, name) for name in os.listdir(os.path.join('src', dir))
    ]
    for name in files:
        with open(name, encoding="utf8") as f:
            text += "\n"
            text += f.read()
    return text


def build_model(source, state_size):
    # Builds a Markov Chain based on source and state_size.
    source = source.split()
    model = {}
    for i in range(state_size, len(source)):
        current_word = source[i]
        previous_words = ' '.join(source[i - state_size:i])
        if previous_words in model:
            model[previous_words].append(current_word)
        else:
            model[previous_words] = [current_word]

    return model


def generate_text(model, state_size, min_length, max_length=50):
    # Generates text based on Markov model.
    # Generates text that is at least <min_length> long and no longer than <max_length>
    def get_new_starter():
        return random.choice([s.split(' ') for s in model.keys() if s[0].isupper()])

    text = get_new_starter()

    i = state_size
    while True:
        key = ' '.join(text[i - state_size:i])
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


# Update the image and the model based which model is active
def update_image(template, source_dir):
    global image_label, img, draw, x_pos_entry, y_pos_entry, font_size_entry, scale_entry, wrap_entry, min_length, max_length
    try:
        x_pos, y_pos = int(x_pos_entry.get()), int(y_pos_entry.get())
        font_size, scale, wrap = int(font_size_entry.get()), float(scale_entry.get()) / 100, int(wrap_entry.get())
    except ValueError:
        return
    state_size = 2
    text = generate_text(build_model(get_source(source_dir), state_size), state_size, int(min_length.get()), int(max_length.get()))
    img = Image.open(template)
    img = img.resize((int(img.width * scale), int(img.height * scale)))
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('FreeMono.ttf', font_size)
    y_pos_scaled = int(y_pos * scale)

    for line in textwrap.wrap(text, wrap):
        draw.text((x_pos * scale, y_pos_scaled), line, font=myFont, fill=(255, 0, 0))
        y_pos_scaled += (font_size + 10) * scale

    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo
    draw = ImageDraw.Draw(img)

# Resets all values
def resetValues():
    for entry in [x_pos_entry, y_pos_entry, font_size_entry, scale_entry, wrap_entry, min_length, max_length]:
        entry.delete(0, tk.END)


# Change the image and model based on the button pressed.
def change_image(which_image):
    global currentModel
    config = {
        1: ("jerma", "JermaTemplate.jpg", "Jerma", (337, 125, 10, 100, 20, 2, 5)),
        2: ("garf", "GarfTemplate.png", "Garfield", (370, 40, 10, 100, 20, 2, 5)),
        3: ("custom", "Custom.png", "Custom", (10, 378, 20, 100, 50, 2, 5))
    }
    if currentModel != config[which_image][0]:
        resetValues()
        x_pos_entry.insert(0, config[which_image][3][0])
        y_pos_entry.insert(0, config[which_image][3][1])
        font_size_entry.insert(0, config[which_image][3][2])
        scale_entry.insert(0, config[which_image][3][3])
        wrap_entry.insert(0, config[which_image][3][4])
        min_length.insert(0, config[which_image][3][5])
        max_length.insert(0, config[which_image][3][6])
        currentModel = config[which_image][0]
    update_image(config[which_image][1], config[which_image][2])

# Save the image to the output folder
def save_image():
    img.save(f"output/{currentModel} Says_{random.randrange(1, 5000)}.png")

# Load in default model and values
currentModel = "jerma"
root = tk.Tk()
img = Image.open("JermaTemplate.jpg")
draw = ImageDraw.Draw(img)
photo = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=photo)
image_label.pack()
frame1 = tk.Frame(root)
frame1.pack()

# UI
tk.Label(frame1, text="X Position:").grid(row=0, column=0)
x_pos_entry = tk.Entry(frame1)
x_pos_entry.insert(0, "337")
x_pos_entry.grid(row=0, column=1)

tk.Label(frame1, text="Y Position:").grid(row=0, column=2)
y_pos_entry = tk.Entry(frame1)
y_pos_entry.insert(0, "125")
y_pos_entry.grid(row=0, column=3)

tk.Label(frame1, text="Font Size:").grid(row=0, column=4)
font_size_entry = tk.Entry(frame1)
font_size_entry.insert(0, "10")
font_size_entry.grid(row=0, column=5)

tk.Label(frame1, text="Scale (%):").grid(row=0, column=6)
scale_entry = tk.Entry(frame1)
scale_entry.insert(0, "100")
scale_entry.grid(row=0, column=7)

frame2 = tk.Frame(root)
frame2.pack()

tk.Label(frame2, text="Text Wrap:").grid(row=1, column=0)
wrap_entry = tk.Entry(frame2)
wrap_entry.insert(0, "20")
wrap_entry.grid(row=1, column=1)

tk.Label(frame2, text="Min Length:").grid(row=1, column=2)
min_length = tk.Entry(frame2)
min_length.insert(0, "2")
min_length.grid(row=1, column=3)

tk.Label(frame2, text="Max Length:").grid(row=1, column=4)
max_length = tk.Entry(frame2)
max_length.insert(0, "5")
max_length.grid(row=1, column=5)

frame3 = tk.Frame(root)
frame3.pack()

change_to_jerma_button = tk.Button(frame3, text="New Jerma Says", command=lambda: change_image(1))
change_to_jerma_button.grid(row=0, column=0, padx=5, pady=5)

change_to_garfield_button = tk.Button(frame3, text="New Garfield Says", command=lambda: change_image(2))
change_to_garfield_button.grid(row=0, column=1, padx=5, pady=5)

frame4 = tk.Frame(root)
frame4.pack()

change_to_funny_button = tk.Button(frame4, text="New Custom", command=lambda: change_image(3))
change_to_funny_button.grid(row=0, column=0, padx=5, pady=5)

save_button = tk.Button(frame4, text="Save Image", command=save_image)
save_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
