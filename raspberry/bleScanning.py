import blescan
import sys
import bluetooth._bluetooth as bluez
import time
import pymysql

dev_id = 0

#pymysql
connection = pymysql.connect(host='...', user = '...', password = '...', db = '...')

try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing Bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    returnedList = blescan.parse_events(sock, 1)
    print "------"
    for beacon in returnedList:
            array = beacon.split(',')
            #seprated ble
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO bleScan(Bname, UUID, MAJOR, MINOR, RSSI, TXpower) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Bname = %s, UUID = %s, MAJOR = %s, MINOR = %s, RSSI = %s, TXpower = %s"
                    cursor.execute(sql, (array[0], array[1], array[2], array[3], array[4], array[5], array[0], array[1], array[2], array[3], array[4], array[5]))
                    #cursor.execute(sql, (array[0], array[1], array[2], array[3], array[4], array[5], array[0], array[1], array[2], array[3], array[4], array[5]))
                
                connection.commit()
                
            finally:
                pass
                #connection.close()
    #print beacon
    
    # stop during 3seconds
    time.sleep(3)
