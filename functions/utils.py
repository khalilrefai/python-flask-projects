IMG_ALLOWED_EXTENSIONS = set(['bmp', 'jpg', 'jpeg', 'pdf', 'png', 'ppm', 'ras', 'sr', 'tif', 'tiff'])
def image_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMG_ALLOWED_EXTENSIONS

