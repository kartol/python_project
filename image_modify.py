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
parser.add_argument('--relief', action='store_true', help='Make relief of the image.')
parser.add_argument('--edges', action='store_true', help='Detect edges of the image.')
parser.add_argument('--blur', action='store_true', help='Make the image blurry.')
parser.add_argument('--sharpen', action='store_true', help='Make the image more sharp.')
parser.add_argument('-o', '--output', help='File name of output image - use a file with *.png', default='output.jpg')


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

# custom conovolve2d - main idea from https://stackoverflow.com/questions/43086557/convolve2d-just-by-using-numpy
def customConvolve2d(array, kernel):
	array = numpy.pad(array,(1,1),'constant')
	return (kernel[0][0] * array[0:-2,0:-2] + kernel[0][1] * array[0:-2,1:-1] + kernel[0][2] * array[0:-2,2:] +
   		    kernel[1][0] * array[1:-1,0:-2] + kernel[1][1] * array[1:-1,1:-1] + kernel[1][2] * array[1:-1,2:] +
            kernel[2][0] * array[2:  ,0:-2] + kernel[2][1] * array[2:  ,1:-1] + kernel[2][2] * array[2:  ,2:])

def imgConvolve(imgArray, kernel):
	r = customConvolve2d(imgArray[:,:,0].astype(numpy.uint32),kernel)
	g = customConvolve2d(imgArray[:,:,1].astype(numpy.uint32),kernel)
	b = customConvolve2d(imgArray[:,:,2].astype(numpy.uint32),kernel)
	return numpy.clip(numpy.dstack([r, g, b]),0,255).astype(numpy.uint8)

def relief(imgArray):
	kernel = numpy.array([[ -2, -1, 0 ],
                          [ -1,  1, 1 ],
                          [  0,  1, 2 ]])
	return imgConvolve(imgArray,kernel)

def detectEdges(imgArray):
	kernel = numpy.array([[ -1, -1, -1 ],
                          [ -1,  8, -1 ],
                          [ -1, -1, -1 ]])
	return imgConvolve(imgArray,kernel)


def blur(imgArray):
	kernel = numpy.array([[ 1, 1, 1 ],
                          [ 1, 1, 1 ],
                          [ 1, 1, 1 ]])/9
	return imgConvolve(imgArray,kernel)



def sharpen(imgArray):
	kernel = numpy.array([[ 0,-1, 0 ],
                          [-1, 5,-1 ],
                          [ 0,-1, 0 ]])
	return imgConvolve(imgArray,kernel)


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

	reliefFlag = args['relief']
	edgeFlag = args['edges']
	blurFlag = args['blur']
	sharpFlag = args['sharpen']

	outputName = args['output']

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

	if(reliefFlag):
		imgArray = relief(imgArray)

	if(edgeFlag):		
		imgArray = detectEdges(imgArray)

	if(blurFlag):
		imgArray = blur(imgArray)

	if(sharpFlag):
		imgArray = sharpen(imgArray)



	# save modified array
	imgOutput = Image.fromarray(imgArray)
	imgOutput.save(outputName)


