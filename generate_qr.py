import qrcode

def generate_qr(image_url, save_path="static/images/qr_code.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(image_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill="black", back_color="white")
    img.save(save_path)
    return save_path