#! /usr/bin/python
#-*- coding: utf-8 -*-


################################
# Programa: GPS Logger com Intel Edison
# Autor: Murilo Ferraz
#
# Inspirado no trabalho de FILIPEFLOP
# blog.filipeflop.com/arduino/usando-o-arduino-gps-shield-com-google-earth.html
#
#################################


import pynmea2
# https://github.com/Knio/pynmea2
import serial
# https://github.com/pyserial/pyserial
import mraa
import time
import pyupm_i2clcd as grove_lcd

# Grove LCD RGB Backlight - i2c
lcd = grove_lcd.Jhd1313m1(0, 0x3E, 0x62)

#### Apresentacao ####
lcd.setCursor(0, 0)
lcd.setColor(255, 0, 0)
lcd.write('#IntelMaker')
lcd.setCursor(1, 0)
lcd.write('Edi GPS Logger')
time.sleep(2)
lcd.clear()
lcd.setCursor(0, 0)
lcd.write('Intel Edison')
lcd.setCursor(1, 0)
lcd.write('iniciando...')
time.sleep(2)
lcd.setColor(0, 0, 255)
####--------####

# Arquivo de texto no qual o log será gravado
fileOut = open('/media/sdcard/output.txt','w')

# Porta serial - pin 0 (RX) - pin 1 (TX)
uart = mraa.Uart(0)

# conforme o datasheet, o modulo ME-X1000RW é 9600 bps
gps = serial.Serial(uart.getDevicePath(), 9600)

#streamreader = pynmea2.NMEAStreamReader()
while(1):
	# ler a saida do gps até o caractere '\n'
    data = gps.readline()
	
	# Escrever no arquivo de text a linha obtida
    fileOut.writelines(data)
	
	# se a linha lida começa com "$GPGGA", então:
	# ps# O modulo gps transmite varios dados de gps
	# porem, somente os dados "$GPGGA" podem ser processadas
	# pela lib pynmea2.
	# leia o datasheet do modulo ME-X1000RW para mais
	# informações
	# ou acesse http://www.gpsinformation.org/dale/nmea.htm
    if data.startswith("$GPGGA"):
        #print data
		
		# evitar um erro desconhecido, depois procuro solução ;)
        coordenadas = data
        msg = pynmea2.parse(coordenadas)
		#msg = pynmea2.parse(data)
		
	#coordenadas processadas, podem ser pesquisadas no google maps
	print (str(msg.latitude) + " " + str(msg.longitude))
	
	# escrever no LCD as coordenadas atuais
	lcd.clear()
	lcd.setCursor(0, 0)
	lcd.write(str(msg.latitude))
	lcd.setCursor(1, 0)
	lcd.write(str(msg.longitude))
	
	
gps.close()
fileOut.close()
