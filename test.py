from matplotlib import pyplot as plt
import numpy as np
import cv2
import collections
import seaborn as sns
count = np.zeros(256, dtype=int)
#print(count)
b = np.arange(25)
img = cv2.imread('dog.jpg', 0)
print(img)
chan = cv2.split(img)
print(chan[0])
for i in chan[0]:
    count[i] += 1
print(count)
xxx = chan[0]/ 10
plt.hist(xxx, bins=25, align='mid')
plt.xlabel('bin')
plt.ylabel('Count')
plt.show()
