import numpy
from PIL import Image

arr = numpy.asarray(Image.open('kvetina.jpg'))

arr = 255 - arr

img = Image.fromarray(numpy.uint8(arr))


img.show()