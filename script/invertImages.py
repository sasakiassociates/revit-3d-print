import os
import sys
import shutil
from PIL import Image
from PIL import ImageOps
import zipfile
import xml.etree.cElementTree as ET

image_folder = sys.argv[1]  # e.g. $python imvertImages.py "C:\\Dynamo\\revit3dprint\\image\\" 2 0.0001
digits = sys.argv[2]
voxelSize = sys.argv[3]


def clean_up(image_folder):  # delete invert, manifest.xml
	files = ["manifest.xml", "model.zip", "model.svx", "invert"]
	for file_name in files:
		file_path = os.path.join(image_folder, file_name)
		if os.path.exists(file_path):
			if os.path.isfile(file_path):
				os.remove(file_path)
			else:
				shutil.rmtree(file_path)


def invert_images(image_folder):
	print("start invert images...")
	origin_image_folder = os.path.join(image_folder, "origin\\")
	print("original image folder: " + origin_image_folder)

	invert_image_folder = os.path.join(image_folder, "invert\\")
	print("inverted image folder: " + invert_image_folder)
	os.makedirs(invert_image_folder)

	for filename in os.listdir(origin_image_folder):
		if os.path.isfile(os.path.join(origin_image_folder, filename)):  # ignore folder
			print("processing image: " + filename)
			image = Image.open(origin_image_folder + filename)
			invert_img = image.convert("RGB")
			inverted_image = ImageOps.invert(invert_img)
			inverted_image.save(invert_image_folder + filename)

	image_name = os.listdir(invert_image_folder)[0]
	image = Image.open(os.path.join(invert_image_folder, image_name))
	width, height = image.size  # get image dimensions
	count = len(os.listdir(invert_image_folder))
	return width, height, count


def create_xml(folder_name, digits, gridSizeX, gridSizeY, gridSizeZ, voxelSize):
	grid = ET.Element("grid")
	channels = ET.SubElement(grid, "channels")
	channels.set("gridSizeX", str(gridSizeX))
	channels.set("gridSizeY", str(gridSizeY))
	channels.set("gridSizeZ", str(gridSizeZ))
	channels.set("voxelSize", str(voxelSize))
	channels.set("subvoxelBits", "8")
	channels.set("originX", "0")
	channels.set("originY", "0")
	channels.set("slicesOrientation", "Y")
	channels.set("originZ", "0")

	channel = ET.SubElement(channels, "channel")
	channel.set("type", "DENSITY")
	channel.set("bits", "8")
	channel.set("slices", "invert/%" + str(digits) + "d.png")

	tree = ET.ElementTree(grid)
	tree.write(os.path.join(folder_name, "manifest.xml"))


def create_zip(folder_name):
	file_name = 'model.zip'
	zip_file = zipfile.ZipFile(os.path.join(folder_name, "model.zip"), 'w', zipfile.ZIP_DEFLATED)
	zip_file.write("manifest.xml", compress_type=zipfile.ZIP_DEFLATED)
	for f_name in os.listdir(os.path.join(folder_name, "invert\\")):
		full_file_path = os.path.join(folder_name, "invert\\" + f_name)
		relative_file_path = os.path.relpath(full_file_path, folder_name)
		zip_file.write(full_file_path, relative_file_path, compress_type=zipfile.ZIP_DEFLATED)
	zip_file.close()
	print("created zip file: " + folder_name + file_name)

	
clean_up(image_folder)
width, height, count = invert_images(image_folder)
create_xml(image_folder, digits, width, height, count, voxelSize)  # todo: match x, y, z order
create_zip(image_folder)
print("done")




