import os
import sys
import shutil
from PIL import Image
from PIL import ImageOps
import zipfile
import xml.etree.cElementTree as ET

image_folder = sys.argv[1]  # e.g. $python imvertImages.py "C:\\Dynamo\\revit3dprint\\image\\" 2 0.0001 6
digits = sys.argv[2]
voxelSize = sys.argv[3]
border = sys.argv[4]


def clean_up(image_folder):  # delete invert, manifest.xml
	files = ["manifest.xml", "model.zip", "model.svx", "invert"]
	for file_name in files:
		file_path = os.path.join(image_folder, file_name)
		if os.path.exists(file_path):
			if os.path.isfile(file_path):
				os.remove(file_path)
			else:
				shutil.rmtree(file_path)


def summary(image_folder):
	image_name = os.listdir(image_folder)[0]
	image = Image.open(os.path.join(image_folder, image_name))
	width, height = image.size  # get image dimensions
	count = len(os.listdir(image_folder))
	return width, height, count


def create_blank_image(image_folder, width, height, file_name):
	image = Image.new('RGB', (width, height), (255, 255, 255))
	image.save(os.path.join(image_folder, file_name))


def crop_images(image_folder, border):
	for file_name in os.listdir(image_folder):
		image_path = os.path.join(image_folder, file_name)
		image = Image.open(image_path)
		cropped_image = ImageOps.expand(image, border=border, fill='white')
		cropped_image.save(image_path)


def invert_images(image_folder):
	print("start invert images...")
	origin_image_folder = os.path.join(image_folder, "origin\\")
	print("original image folder: " + origin_image_folder)

	invert_image_folder = os.path.join(image_folder, "invert\\")
	print("inverted image folder: " + invert_image_folder)
	os.makedirs(invert_image_folder)

	for file_name in os.listdir(origin_image_folder):
		image_path = os.path.join(origin_image_folder, file_name)
		if os.path.isfile(image_path):  # ignore folder
			print("processing image: " + file_name)
			image = Image.open(origin_image_folder + file_name)
			invert_img = image.convert("RGB")
			inverted_image = ImageOps.invert(invert_img)
			inverted_image.save(invert_image_folder + file_name)


def create_xml(folder_name, digits, gridSizeX, gridSizeY, gridSizeZ, voxelSize):
	grid = ET.Element("grid")
	grid.set("gridSizeX", str(gridSizeX))
	grid.set("gridSizeY", str(gridSizeY))
	grid.set("gridSizeZ", str(gridSizeZ))
	grid.set("voxelSize", str(voxelSize))
	grid.set("subvoxelBits", "8")
	grid.set("originX", "0")
	grid.set("originY", "0")
	grid.set("slicesOrientation", "Y")
	grid.set("originZ", "0")

	channels = ET.SubElement(grid, "channels")
	channel = ET.SubElement(channels, "channel")
	channel.set("type", "DENSITY")
	channel.set("bits", "8")
	channel.set("slices", "invert/%0" + str(digits) + "d.png")

	tree = ET.ElementTree(grid)
	tree.write(os.path.join(folder_name, "manifest.xml"))


def create_zip(folder_name):
	file_name = 'model.zip'
	zip_file = zipfile.ZipFile(os.path.join(folder_name, "model.zip"), 'w', zipfile.ZIP_DEFLATED)
	zip_file.write(os.path.join(folder_name, "manifest.xml"), "manifest.xml", compress_type=zipfile.ZIP_DEFLATED)
	for f_name in os.listdir(os.path.join(folder_name, "invert\\")):
		full_file_path = os.path.join(folder_name, "invert\\" + f_name)
		relative_file_path = os.path.relpath(full_file_path, folder_name)
		zip_file.write(full_file_path, relative_file_path, compress_type=zipfile.ZIP_DEFLATED)
	zip_file.close()
	print("created zip file: " + folder_name + file_name)


clean_up(image_folder)

origin_image_folder = os.path.join(image_folder, "origin")
width, height, count = summary(origin_image_folder)

start_image_name = str(0).rjust(int(digits), '0') + ".png"
end_image_name = str(count + 1).rjust(int(digits), '0') + ".png"
create_blank_image(origin_image_folder, width, height, start_image_name)
create_blank_image(origin_image_folder, width, height, end_image_name)

crop_images(origin_image_folder, int(border))
invert_images(image_folder)
create_xml(image_folder, digits, width, count + 2, height, voxelSize)
create_zip(image_folder)
print("done")




