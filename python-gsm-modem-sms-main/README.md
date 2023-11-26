# python-sms-modem
GSM modem module for Python

python-sms-modem is a program that allow sending and receiving sms using gsm modem or broadband module

* features 

Functions for sending messages and receiving message
allows handling of AT commands 

* Files:

sms: easy to use python script with functions for sending and receiving sms .
ports.py: Script used to print all ports and devices attached to

* How to use this package

Identify port attached to the modem
py ports.py 
This will list all ports and identify the ports attached with modem example C0M30 then modify sms.py if port is no 30 for windows

py sms.py 
Use methods on this file for sending and receiving text messages 
