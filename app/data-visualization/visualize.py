import matplotlib.pyplot as plt
import db
def drawGraphs():
    data=getStoredData()
    time=[]
    temp=[]
    most=[]
    light=[]
    if data!=None :
        for i in data:
            temp.append(i[0])
            most.append(i[1])
            light.append(i[2])
            time.append(i[3])
    plt.plot(time, temp, 'ro', time, most,'g^', time, light, 'c--')
    #plt.axis([0, 20, 0,24])
    plt.ylabel('Temperature/ Moisture/ light')
    plt.xlabel('Time')
    plt.show()



import matplotlib.pylab as plt
import numpy as np

def get_coord(table, irow, icol):
    cell = table.get_celld()[irow+1,icol]
    box = cell.get_bbox().get_points()
    xc, yc = box.mean(axis=0)
    return xc, yc

col_labels=['G','A','T','C','C']
row_labels= ['G','T','G','C','C']
table_vals= [
    ['x','','','',''],
    ['','','x','',''],
    ['x','','','',''],
    ['','','','x','x'],
    ['','','','x','x']]
line = [(0,0), (0,1), (1,2), (2,2), (3,3), (4,4)]

the_table = plt.table(cellText=table_vals,
    colWidths = [0.1]*len(col_labels),
    rowLabels=row_labels, colLabels=col_labels,
    cellLoc = 'center', rowLoc = 'center', bbox=[.1,.1,.8,.8])
plt.draw()

x = []; y = []
for irow, icol in line:
    xc, yc = get_coord(the_table, irow, icol)
    x.append(xc)
    y.append(yc)

# draw line
plt.plot(x, y, 'r', linewidth = 5, alpha=0.5)
plt.xlim([0,1])
plt.ylim([0,1])
plt.show()
