import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

func = []
dataset = ['8', '7','6', '5', '4', '3', '2', '1']
im = image.imread('crop.png')
fig, ax = plt.subplots()
ax.imshow(im, aspect='auto', extent=(1, 5, 0, 1.001))
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
    if dataset[i] == '8':
        degree = 14
    else:
        degree = 6
    polyfit = np.poly1d(np.polyfit(x, y, degree))
    print(polyfit)
    x = np.arange(1, 5, 0.001)
    y = polyfit(x)
    plt.plot(x, y)

plt.show()