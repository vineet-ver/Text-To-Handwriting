from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os, io, textwrap, img2pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/output'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    fonts = os.listdir('static/fonts')
    return render_template('index.html', fonts=fonts)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    color = request.form['color']
    font_choice = request.form['font']

    font_path = os.path.join('static/fonts', font_choice)
    font = ImageFont.truetype(font_path, 48)

    lines = textwrap.wrap(text, width=40)
    line_height = font.getbbox("A")[3] + 10
    img_height = line_height * len(lines) + 100

    img = Image.new("RGB", (1200, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    y = 50

    for line in lines:
        draw.text((60, y), line, font=font, fill=color)
        y += line_height

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], "handwriting.png")
    img.save(output_path)

    # Optional: convert to PDF
    pdf_path = output_path.replace('.png', '.pdf')
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(output_path))

    return render_template('index.html', img=output_path, pdf=pdf_path, fonts=os.listdir('static/fonts'))

if __name__ == '__main__':
    app.run(debug=True)
