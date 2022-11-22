import extcolors
from colormap.colors import rgb2hex
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import pandas as pd


UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
test_img_path = 'static/images/'
total_percent = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap(app)

total_px = 0
hex_colors = []

# extract color from image
colors, pixel_count = extcolors.extract_from_path("static/images/test.jpg", tolerance = 12, limit = 12)
# print(colors)

# cut length to 8
# if len(colors) > 8:
#     colors = colors[0:8]
#     print(f'new string: {colors}')
# else:
#     print(f'default string: {colors}')

# print(colors[0:][0][1])


# store total percent in variable for percentage calculation
for k in range(len(colors)):
    total_percent += colors[0:][1][1]

# convert rgb into hex and store in a list
for i in range(len(colors)):
    total_px += colors[0:][i][1]
    percent = ( colors[0:][i][1] / total_percent ) * 100
    # print(colors[0:][i][0])
    hex_colors.append(rgb2hex(colors[0:][i][0][0], colors[0:][i][0][1], colors[0:][i][0][2]))
    # print(hex_colors)
    # print(f'{percent :.2f}%')

# store length of colors into new variables, because flask cannot use len() function with html
length_of_color = len(colors)

## check variables
# print(total_px)
# print(total_percent)
# print(hex_colors)

# for i in hex_colors:
#     print(i)

# print(hex_colors)


@app.route("/", methods=['GET', 'POST'])
def home():
    # files = [f for f in os.listdir("static/images") if os.path.isfile(os.path.join("static/images", f))]
    # for file in files:
    #     if file != test_img_path:
    #         os.remove(f"static/images/{file}")
    return render_template("index.html", colors = colors, total_percent = total_percent, length = length_of_color, hex_colors = hex_colors)


@app.route('/<prev_filename>', methods=['GET', 'POST'])
def upload_image(prev_filename):
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'File uploaded successfully!'

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)