from flask import Flask, request, send_file, render_template
import qrcode
from PIL import Image
import os

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate the QR code
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    url = request.form['url']
    fill_color = request.form['color']
    
    logo = request.files.get('logo')
    logo_path = None

    # If a logo is uploaded, save it temporarily
    if logo:
        logo_path = os.path.join('temp_logo.png')
        logo.save(logo_path)
    
    # Generate the QR code
    qr_img = create_custom_qr(url, fill_color, logo_path)

    # Save the generated QR code as a file
    qr_img.save('generated_qr.png')

    # Return the image to the user
    return send_file('generated_qr.png', mimetype='image/png')

def create_custom_qr(url, fill_color, logo_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction to allow for logo
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create the QR code with the selected color
    img = qr.make_image(fill_color=fill_color, back_color="white").convert('RGB')

    # If a logo is provided, overlay it
    if logo_path:
        logo = Image.open(logo_path)
        logo_size = (img.size[0] // 4, img.size[1] // 4)  # Resize logo to 1/4 of QR code
        logo = logo.resize(logo_size)

        # Calculate position to paste the logo (center of QR code)
        logo_position = ((img.size[0] - logo_size[0]) // 2, (img.size[1] - logo_size[1]) // 2)
        img.paste(logo, logo_position, mask=logo)

    return img

if __name__ == '__main__':
    app.run(debug=True)
