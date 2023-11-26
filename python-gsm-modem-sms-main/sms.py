import serial
import time
import sys


ser = serial.Serial('COM5', 115200, timeout=12)   #initialize modem com port 

def SendCommand(command, getline=True):

    #print(command)
    ser.write(command.encode())
    time.sleep(2)
    response = ''
    if getline:
        response=ReadLine()
        return(response) 

def ReadLine():
    response = ser.readline()
    print (response)
    return response 



def ReceiveSms():
    SendCommand('ATZ\r')
    SendCommand('AT+CMGF=1\r')
    ser.flushInput()
    ser.flushOutput()
    SendCommand('AT\r')
    command = 'AT+CMGL="REC UNREAD"\r'                  #gets sms that has not been read
    #print (SendCommand(command, getline=True))
    response = ser.readall()                            #read response from serial
    response=str(response)
    #print(response)
    if "REC UNREAD" in response:
        numberIndex=response.find('+255')  
        smsIndex=response.find('"\\r\\n')+5
        smsLastIndex=response.find('\\r\\n\\r\\nOK\\r\\n')
        phone=response[numberIndex:numberIndex+13]
        sms=response[smsIndex:smsLastIndex]
        print("Phone:"+phone)
        print("sms :" +sms)

        return(phone,sms)


def SendSms(message,to):
      SendCommand('ATZ\r')
      SendCommand('AT+CMGF=1\r')
      to='AT+CMGS='+'"'+to+'"'

      SendCommand('ATE0\r')

      SendCommand('AT\r')
      
      SendCommand('AT+CMGD="ALL"\r')

      SendCommand('AT+CMGF=1\r')

      SendCommand(to + "\r")

      SendCommand(message + "\r")

      SendCommand(chr(26))

      print ("disconnecting")
      ser.flush()
      ser.close()


print(ReceiveSms())