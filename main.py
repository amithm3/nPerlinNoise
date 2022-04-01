from perlin import *

import PIL
import cv2
from matplotlib import pyplot

noise = Perlin3D(3)

# fig = pyplot.figure()
# pyplot.plot(noise.noise(np.arange(0, 200), np.ones(200) * 1, checkFormat=False))
# pyplot.show()
#
# fig = pyplot.figure()
# x = np.arange(0, 200)
# pyplot.imshow([noise.noise(x, np.ones(len(x)) * i, checkFormat=False) for i in range(200)])
# pyplot.show()
#