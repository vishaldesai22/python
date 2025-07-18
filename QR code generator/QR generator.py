# Import the qrcode library to generate QR codes
import qrcode

# Import the Image class from the PIL (Pillow) library to work with images
from PIL import Image

# Create a QRCode object with specific settings
qr = qrcode.QRCode(
    version=1,  # Version 1 means the QR code will be 21x21 modules (smallest size)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction (H = ~30% of data can be recovered if damaged)
    box_size=10,  # Each box of the QR code will be 10x10 pixels
    border=10     # Add a border of 10 boxes around the QR code (minimum is 4)
)

# Add the data (YouTube link) that should be encoded into the QR code
qr.add_data("https://www.youtube.com/watch?v=FOGRHBp6lvM&list=WL&index=2")

# Finalize the QR code (adjusts the size automatically to fit the data)
qr.make(fit=True)

# Create the QR code image with a custom color
# fill_color is the color of the squares (QR pattern)
# back_color is the background color of the QR code
img = qr.make_image(fill_color="skyblue", back_color="white")

# Save the QR code image to a file named 'youtube.png'
img.save("youtube.png")
