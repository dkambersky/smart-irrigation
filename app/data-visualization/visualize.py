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
