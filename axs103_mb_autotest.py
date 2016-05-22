import time
import serial

#how to use:
#
#connect to board: (windows)
#createConnection('COM13')
#connect to board: (linux)
#createConnection('/dev/ttyUSB0')
#
#run as many test attempt as needed:
#test(100)


ser = serial.Serial()


#use COM13 for windows
#or
#use /dev/ttyUSB0 for linux
def createConnection(uart_port = 'COM13'):
    global ser
    try: 
        ser = serial.Serial(
            port = uart_port,
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0.1
        )
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()


def execCmd(cmd, attempts, wait_time):
    global ser
    response = ""
    if ser.isOpen():
        try:
            ser.flushInput()
            ser.flushOutput()
            ser.write(cmd)
            time.sleep(wait_time)
            for i in range(0, attempts):
                responsBuff = ser.readline()
                if(responsBuff):
                    response += str(responsBuff)
#            print(">>>: " + response)
            
        except Exception as e1:
            print("error communicating...: " + str(e1))

    else:
        print ("error: port closed")
        
    return response
        

def dhcpStat(memAdr):
    response = execCmd((b'dhcp ' + memAdr + b"\n"), 40, 5)
    status = "FAIL UNKNOWN"
    if(response.find("done") != -1):
        response = execCmd(b"iminfo\n", 10, 2)
        if(response.find("OK") != -1):
            status = "OK"
        if(response.find("CRC") != -1):
            status = "CRC FAIL"
    else:
        if(response.find("BOOTP") != -1):
            status = "DHCP TIMEOUT FAIL"
    
    return status

        
def test(attempts = 10):
    memAddr1 = b"0x82000000"
    memAddr2 = b"0x82000004"
    for i in range(attempts):
        if(i % 2 == 0):
            loadAddr = memAddr1
        else:
            loadAddr = memAddr2
        status = dhcpStat(loadAddr)
        print(status + " addr: " + str(loadAddr))
        
        
def closeConnection():
    ser.close()
            
            
            
            
            
            
            
            
            
            
            