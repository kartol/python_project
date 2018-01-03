import numpy
from PIL import Image
import sys
import argparse


parser = argparse.ArgumentParser(description='This program modifies an image, it can make severals modifications in one run and this modifications will be made in order given by help eg. it will make inverse first and then rotation because inverse is in help before the rotation. You cannot specify the order of actions but you can run this program severals time with subset of actions you want to make in total to get desired efect.')
parser.add_argument('file', type=str,  help='Input image file')
parser.add_argument('-i', '--inverse',  action='store_true', help='Use this argument if you want to inverse color of processing image.')
parser.add_argument('-r', '--rotate', type=int, help='Rotate the image to the left - you can specify number of rotates.')
parser.add_argument('-g', '--gray', action='store_true', help='Make the image gray.')
parser.add_argument('-d', '--darken', type=int,  help = "Make the image darker by given value - it multiples values in pixels - 10 is like 10 %% darker" )
parser.add_argument('-l', '--lighten', type=int,  help = "Make the image lighter by given value - it multiples values in pixels - 10 is like 10 %% lighter")
parser.add_argument('-f', '--flip', type=int, help = "Flip the image - insert 0 for vertical flip or 1 for horizontal")


def inverse(imgArray):
	return 255 - imgArray

def rotate(imgArray,times = 1):
	return numpy.rot90(imgArray,times)

def grayscale(imgArray):
	imgArray = imgArray * numpy.array([0.299,0.587,0.144])
	imgArray = imgArray.sum(2)
	return imgArray


def darken(imgArray,value):
	return numpy.clip(( (1 - value/100) * imgArray),0,255).astype(numpy.uint8)


def lighten(imgArray,value):
	return numpy.clip(( (1 + value/100) * imgArray),0,255).astype(numpy.uint8)

def flip(imgArray,direction):
	if(direction == 1):
		return imgArray[::-1,...]
	return imgArray[:,::-1]


''' 
	I am not sure if I should make a class for image with inverse methods and so one
	or if should i make just few methods that can process pixel array
'''

if __name__ == "__main__":
	args = vars(parser.parse_args())
	fileName = args['file']
	inverseFlag = args['inverse']
	rotateFlag = True if args['rotate'] else False
	rotateTimes = args['rotate']

	grayscaleFlag = args['gray']

	darkenFlag = True if args['darken'] else False
	darkenScale = args['darken']


	lightenFlag = True if args['lighten'] else False
	lightenScale = args['lighten']

	flipFlag = True if not ( args['flip'] is None ) else False
	if(flipFlag):
		flipDirection = args['flip']%2

	# extract array from input image

	imgArray = numpy.asarray(Image.open(fileName))

	if(inverseFlag):
		imgArray = inverse(imgArray)


	if(rotateFlag):
		imgArray = rotate(imgArray,rotateTimes)

	if(grayscaleFlag):
		imgArray = grayscale(imgArray)

	if(darkenFlag):
		imgArray = darken(imgArray,darkenScale)


	if(lightenFlag):
		imgArray = lighten(imgArray,lightenScale)

	if(flipFlag):
		imgArray = flip(imgArray,flipDirection)

	# process the modified array
	imgOutput = Image.fromarray(imgArray)
	imgOutput.show()


