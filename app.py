from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No se ha seleccionado ningún archivo.')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No se ha seleccionado ningún archivo.')
        
        img = Image.open(file)
        img_path = f'static/{file.filename}'
        img.save(img_path)
        
        output_path = f'static/{file.filename}_no_bg.png'
        
        with open(img_path, 'rb') as f:
            input_data = f.read()
        
        output_data = remove(input_data)
        
        with open(output_path, 'wb') as out_file:
            out_file.write(output_data)
        
        return render_template('index.html', original_img=img_path, result_img=output_path)

    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_file(f'static/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
