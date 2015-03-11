# -*- coding:utf-8 -*-
import os,os.path
import shutil
import hashlib

def _get_qr_url(appId,app_apk_url,logo_url=''):
    directory = 'static/qrdata/{f1}/{f2}/'.format(f1=appId/100000,f2=(appId%100000)/2000)
    qr_path = os.path.join(app.config['ROOT_PATH'],directory)
    if not os.path.exists(qr_path):
        os.makedirs(qr_path)

    md5File = '%s.png' % hashlib.md5(app_apk_url).hexdigest()
    qr_file = '%s%s' % (qr_path,md5File)
    qr_url = directory + md5File
    if os.path.exists(qr_file):
        return qr_url
    else:
        import qrcode
        from PIL import Image

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=2
        )
        qr.add_data(app_apk_url)
        qr.make(fit=True)
        img = qr.make_image()
        img = img.convert("RGBA")

        logo_file = _get_apk_logo(appId,logo_url)
        if logo_file and os.path.exists(logo_file):
            icon = Image.open(logo_file)
            img_w, img_h = img.size
            factor = 4
            size_w = int(img_w / factor)
            size_h = int(img_h / factor)

            icon_w, icon_h = icon.size
            if icon_w > size_w:
                icon_w = size_w
            if icon_h > size_h:
                icon_h = size_h
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

            w = int((img_w - icon_w) / 2)
            h = int((img_h - icon_h) / 2)
            icon = icon.convert("RGBA")
            img.paste(icon, (w, h), icon)

        img.save(qr_file)
    return qr_url