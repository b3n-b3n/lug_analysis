import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

func = []
dataset = [str(i) for i in range(1, 12)]
im = plt.imread('crop_bigger.png')
fig, ax = plt.subplots()
ax.imshow(im, aspect='auto', extent=(0, 1.4, 0, 1.7))
ax.tick_params(axis='y', colors='black', labelsize=10)
ax.tick_params(axis='x', colors='black', labelsize=10)
plt.ylim(0, 1.7)
plt.xlim(0, 1.4)
#plt.xticks(x, my_xticks)
#plt.yticks(0, 0.9)



for i in range(len(dataset)):
    data = open('L'+dataset[i]).readlines()
    data = [float(d.strip()) for d in data]

    b = open('B'+dataset[i]).readline()
    b = float(b.strip())

    X = np.linspace(0, b, 100)
    Y = []
    for j in range(len(X)):
        y = 0 
        degree = len(data)-1
        for k in range(len(data)):
                y += data[k] * X[j]**(degree-k)
        Y.append(y)
    plt.plot(X, Y)

    
    #------------------------------------------------------------------------------
    if b != 1.4:
        data = open('R'+dataset[i]).readlines()
        data = [float(d.strip()) for d in data]
    
        X2 = np.linspace(b, 1.4, 100)
        Y2 = []
        for j in range(len(X2)):
            y = 0 
            degree = len(data)-1
            for k in range(len(data)):
                y += data[k] * X2[j]**(degree-k)
            Y2.append(y)
        plt.plot(X2, Y2)

plt.show()