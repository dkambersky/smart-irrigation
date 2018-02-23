import redis

try:
    conn = redis.StrictRedis(host='cloudgamma.redis.cache.windows.net', port=6379,password='rrpfHJ8YglYS69M03iG4IoBgc8gUiksr1Pf4qrBfutQ=')

    print (conn)
    conn.ping()
    print ('Connected!')
    ssl=True,
    ssl_ca_certs='LOCAL/PATH/TO/rackspace-ca-2016.pem'
except Exception as ex:
    print ('Error:', ex)

    conn.rpush('temp')
    conn.rpush('most')
    conn.rpush('light')
    conn.rpush('time')
    conn.set(",auto_number")

def storeData( temp, most, light, arr_time):

    try:
        conn.rpush('temp', temp)
        conn.rpush('most', most)
        conn.rpush('light',light)
        conn.rpush('time',arr_time)
        conn.incr("auto_number")
    except:
        print(" something went wrong")



    #this return all stored data in caches as an array of [[temp, most, light, time]]
def getStoredData():
    a=conn.lrange('temp',0, -1)
    b=conn.lrange('most',0, -1)
    c=conn.lrange('light',0, -1)
    d=conn.lrange('time',0, -1)

    counter=1
    arr=[]
    for i in range(len(a)):
        arr.append([])
        arr[i].append(a[i])
        arr[i].append(b[i])
        arr[i].append(c[i])
        arr[i].append(d[i])

    return arr

def deleteAll():
    x = conn.keys()
    for key in x: conn.delete(key)
