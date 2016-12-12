import os
from PIL import Image
from PIL import ImageOps

cmdargs = str(sys.argv)

dir = cmdargs[0]
dir =+ "\"

filename = cmdargs[1]

image = Image.open(dir + filename)
invert_im = image.convert("RGB")
inverted_image = ImageOps.invert(invert_im)
inverted_image.save(dir + "invert_" + filename)

width, height = inverted_image.size  # Get dimensions
left = 680
top = 800
right = 3456 - 680
bottom = 3456 - 1000
cropped_image = inverted_image.crop((left, top, right, bottom))
cropped_image.save(dir + "crop_" + filename)