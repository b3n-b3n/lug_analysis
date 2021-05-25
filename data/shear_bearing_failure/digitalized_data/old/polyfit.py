import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

func = []
dataset = ['30', '25', '20', '15', '10', '9', '8', '7',
        '6', '5', '4', '3']
im = image.imread('table0.png')
fig, ax = plt.subplots()
ax.imshow(im, aspect='auto', extent=(0.6, 4, 0, 3))
ax.tick_params(axis='y', colors='black', labelsize=10)
ax.tick_params(axis='x', colors='black', labelsize=10)


for i in range(len(dataset)):
    data = open(dataset[i]).readlines()
    x = []
    y = []
    for j in range(len(data)):
        data[j] = data[j].strip('\n').split(',')
        x.append(float(data[j][0]))
        y.append(float(data[j][-1]))
    degree = 6
    polyfit = np.poly1d(np.polyfit(x, y, degree))
    print(polyfit)
    x = np.arange(0.6, 4, 0.01)
    y = polyfit(x)
    plt.plot(x, y)

plt.show()