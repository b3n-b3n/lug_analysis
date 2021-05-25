import numpy as np

func = []
dataset = ['30', '25', '20', '15', '10', '9', '8', '7',
        '6', '5', '4', '3']
deg = [6, 5, 5, 8, 5, 8, 5, 5, 5, 7, 5, 6]
for i in range(len(dataset)):
    data = open(dataset[i]).readlines()
    x = []
    y = []
    for j in range(len(data)):
        data[j] = data[j].strip('\n').split(',')
        x.append(float(data[j][0]))
        y.append(float(data[j][-1]))
    degree = deg[i]
    polyfit = np.polyfit(x, y, degree)
    file = open("n{}".format(dataset[i]), "w") 
    for j in range(len(polyfit)):
        file.write(str(round(polyfit[j], 10)) + '\n') 
    file.close() 
    print(polyfit)