from machine import Pin, UART
import utime, time

loc = []

gpsModule = UART(1, baudrate=38400, tx=Pin(4), rx=Pin(5))

buff = bytearray(255)
latitude = ""
longitude = ""
satellites = ""
GPStime = ""

list_of_tuples = []
list_of_times = []

def FirstTwoListItems(str_list):
    current_num = 0
    for list_i in range(len(str_list)):
        try:
            int_str_list = int(str_list[list_i])
            current_num += 1
            if current_num == 2:
                tup_var = (num, int_str_list)
                return tup_var
            else:
                num = int_str_list
                tup_var = (num)
        except:
            pass


while True:
    start_time = time.time()

    gpsModule.readline()
    buff = str(gpsModule.readline())
    buff = str(gpsModule.read())
    parts = buff.split(',')
    print(parts)
    
    
    for i in range(len(parts)):
        if "GNGLL" in parts[i]:
            print("KYLE /n IS REALY REALLY REALLY REALLY REALLY REALLY REALLY /n REALLY REALLY REALLY COOL")
            
            list_of_tuples.append(FirstTwoListItems(parts[i]))
            
            loc.append(str(parts))
            print(loc)
    end_time = time.time()
    list_of_times.append(int(end_time - start_time))
    print(list_of_times)
    utime.sleep_ms(500)