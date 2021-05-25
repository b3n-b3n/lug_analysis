import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

func = []
# dataset = ['1', '2', '3', '4', '5']
dataset = ['8']
im = plt.imread('crop2.png')
fig, ax = plt.subplots()
ax.imshow(im, aspect='auto', extent=(0, 1.4, 0, 1.7))
ax.tick_params(axis='y', colors='black', labelsize=10)
ax.tick_params(axis='x', colors='black', labelsize=10)


for i in range(len(dataset)):
    data = open('L'+dataset[i]).readlines()
    X = []
    Y = []
    for j in range(len(data)):
        data[j] = data[j].strip('\n').split(',')
        X.append(float(data[j][0]))
        Y.append(float(data[j][-1]))
    degree = 4
    polyfit = np.poly1d(np.polyfit(X, Y, degree))
    x = np.arange(0, X[-1], 0.001)
    y = polyfit(x)
    plt.plot(x, y)
   # print(polyfit)
    #print(X[-1])
    
    #------------------------------------------------------------------------------

    data = open('R'+dataset[i]).readlines()
    X2 = []
    Y = []
    for j in range(len(data)):
        data[j] = data[j].strip('\n').split(',')
        X2.append(float(data[j][0]))
        Y.append(float(data[j][-1]))
    degree = 6
    polyfit = np.poly1d(np.polyfit(X2, Y, degree))
    x = np.arange(X[-1], 1.40, 0.001)
    y = polyfit(x)
    plt.plot(x, y)
    print(list(polyfit))
plt.show()