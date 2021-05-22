import numpy as np

dataset = ['8', '7', '6', '5', '4', '3', '2','1']

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
        degree = 5
    
    polyfit = np.polyfit(x, y, degree)
    file = open("n{}".format(dataset[i]), "w") 
    for j in range(len(polyfit)):
        file.write(str(round(polyfit[j], 10)) + '\n') 
    file.close() 
    print(polyfit)