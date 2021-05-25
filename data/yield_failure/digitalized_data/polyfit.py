import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

im = image.imread('crop.PNG')
fig, ax = plt.subplots()
ax.imshow(im, aspect='auto', extent=(0, 3, 0.5, 1.1))
ax.tick_params(axis='y', colors='black', labelsize=10)
ax.tick_params(axis='x', colors='black', labelsize=10)
ax.set_ylim(0.5, 1.1)


data = open('yield2').readlines()
x = []
y = []
for j in range(len(data)):
    # data[j] = data[j].strip('\n').replace(',', '.').split(' ')
    data[j] = data[j].strip('\n').split(', ')
    x.append(float(data[j][0]))
    y.append(float(data[j][-1]))
degree = 6
polyfit = np.poly1d(np.polyfit(x, y, degree))
for x in polyfit:
    print(x)
x = np.arange(1.15, 3, 0.01)
y = polyfit(x)
plt.plot(x, y)
plt.show()