from imu import MPU6050
import time
import math
from machine import Pin, I2C, UART, ADC
from bmp280 import *
from dht import DHT11
from calculos_gas import Calculos


uart = UART(1, 9600, rx = Pin(5), tx = Pin(4))

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

ledInterno = Pin(25, Pin.OUT)
ledInterno.value(0)

ERROR = -3 # hPa
# crecion del objeto BMP
bmp280_object = BMP280(i2c,
                       addr = 0x76, # change it 
                       use_case = BMP280_CASE_WEATHER)

bmp280_object.power_mode = BMP280_POWER_NORMAL
bmp280_object.oversample = BMP280_OS_HIGH
bmp280_object.temp_os = BMP280_TEMP_OS_8
bmp280_object.press_os = BMP280_TEMP_OS_4
bmp280_object.standby = BMP280_STANDBY_250
bmp280_object.iir = BMP280_IIR_FILTER_2

print("BMP Object created successfully !")


def altitude_HYP(hPa , temperature):
    # Hypsometric Equation (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 # hPa      
    pressure_ratio = sea_level_pressure/local_pressure # sea level pressure = 1013.25 hPa
    h = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return h


# altitude from international barometric formula, given in BMP 180 datasheet
def altitude_IBF(pressure):
    local_pressure = pressure    # Unit : hPa
    sea_level_pressure = 1013.25 # Unit : hPa
    pressure_ratio = local_pressure / sea_level_pressure
    altitude = 44330*(1-(pressure_ratio**(1/5.255)))
    return altitude

MQ_9 = ADC(26)
MQ_135 = ADC(27)

factor_16 = 3.3 / 65535
factor_10 = 3.3/1024

'''-- MQ-9 conversion --'''
# Ro value of the sensor
ro_MQ_9 = 0.943
# Curva logaritmica con base 10
CO_CURVA = [2.301030, 0.227887, -0.478819]
GPL_CURVA = [2.301030, 0.324282, -0.471955]
# gas en ppm
co_ppm = 0
gpl_ppm = 0
calculo_MQ_9 = Calculos()
'''--------------------------------------'''

'''MQ-135 conversion'''
# Ro value of the sensor
ro_MQ_135 = 1.521
# Curva logaritmica con base 10
ACETONA_CURVA = [1, 0.178977, -0.319976]
TOLUENO_CURVA = [1, 0.209515, -0.312630]
ALCOHOL_CURVA = [1, 0.283301, -0.321436]
# gas en ppm
acetona_ppm = 0
tolueno_ppm = 0
alcohol_ppm = 0
calculo_MQ_135 = Calculos()
'''--------------------------------------'''


# position
xo = 0.00
yo = 0.00
zo = 0.00
acc      = {'x': 0.00, 'y': 0.00, 'z':0.00}
a_act    = {'x': 0.00, 'y': 0.00, 'z':0.00}
a_bef    = {'x': 10.00, 'y': 10.00, 'z':10.00}
a_dif    = {'x': 0.00, 'y': 0.00, 'z':0.00}
position = {'x': 0.00, 'y': 0.00, 'z':0.00}
vel      = {'x': 0.00, 'y': 0.00, 'z':0.00}
vel_aux  = {'x': 0.00, 'y': 0.00, 'z':0.00}
vel_dif  = {'x': 0.00, 'y': 0.00, 'z':0.00}

def check_mpu():
    sensor = MPU6050(i2c)  
    return sensor

while True:
    # Adquisición de temperatura
    temperatura = bmp280_object.temperature # degree celcius
    # Adquisición de presion
    presion = bmp280_object.pressure  # pascal
    ledInterno.value(1)
    # DHT11
    try:
        dht_pin = Pin(18, Pin.OUT, Pin.PULL_DOWN)
        sensor_hum = DHT11(dht_pin)
        humedad = (sensor_hum.humidity)
    except(NameError):
        print("")
        
        
    '''-- MQ-9 conversion --'''
    V_MQ_9 = calculo_MQ_9.calcular_voltaje(MQ_9.read_u16(),factor_16)
    rs_MQ_9 = calculo_MQ_9.calcular_resistencia(V_MQ_9,1)
    ratio_MQ_9 = rs_MQ_9 / ro_MQ_9
    co_ppm = calculo_MQ_9.calcular_ppm(ratio_MQ_9,CO_CURVA)
    gpl_ppm = calculo_MQ_9.calcular_ppm(ratio_MQ_9,GPL_CURVA)


    '''-- MQ-135 conversion --'''
    V_MQ_135 = calculo_MQ_135.calcular_voltaje(MQ_135.read_u16(),factor_16)
    rs_MQ_135 = calculo_MQ_135.calcular_resistencia(V_MQ_135,1)
    ratio_MQ_135 = rs_MQ_135 / ro_MQ_135
    acetona_ppm = calculo_MQ_135.calcular_ppm(ratio_MQ_135,ACETONA_CURVA)
    tolueno_ppm = calculo_MQ_135.calcular_ppm(ratio_MQ_135,TOLUENO_CURVA)
    alcohol_ppm = calculo_MQ_135.calcular_ppm(ratio_MQ_135,ALCOHOL_CURVA)


    vel_aux['x'] = vel['x']
    vel_aux['y'] = vel['y']
    vel_aux['z'] = vel['z']
    
    try:
        imu = check_mpu()
        acc['x'] = round(imu.accel.x, 2)
        acc['y'] = round(imu.accel.y, 2)
        acc['z'] = round(imu.accel.z, 2)
        #acc    = sensor.read_accelerometer()#get_accel_data()
        vel['x'] = round(imu.gyro.x, 2)
        vel['y'] = round(imu.gyro.y, 2)
        vel['z'] = round(imu.gyro.z, 2)
    except(OSError):
        acc = {'x': 0.00, 'y': 0.00, 'z': 0.00}
        vel = {'x': 9999.99, 'y': 9999.99, 'z': 999.99}
        print("MPU desconectado")
    try:
        imu = check_mpu()
        acc['x'] = round(imu.accel.x, 2)
        acc['y'] = round(imu.accel.y, 2)
        acc['z'] = round(imu.accel.z, 2)
        #acc    = sensor.read_accelerometer()#get_accel_data()
        vel['x'] = round(imu.gyro.x, 2)
        vel['y'] = round(imu.gyro.y, 2)
        vel['z'] = round(imu.gyro.z, 2)
        
        a_act['z'] = math.atan(acc['z']/math.sqrt(pow(acc['x'],2)+pow(acc['y'],2)))*(180/3.1416)
        a_act['y'] = math.atan(acc['y']/math.sqrt(pow(acc['x'],2)+pow(acc['z'],2)))*(180/3.1416)
        a_act['x'] = math.atan(acc['x']/math.sqrt(pow(acc['z'],2)+pow(acc['y'],2)))*(180/3.1416)
        #print(sensor.get_temp())
        print(vel)
        print(vel_aux)
        print(acc)
        print(str(position))
        print("Dioxido de Carbono:" ,co_ppm)
        print("Gas Natural: ",gpl_ppm)
        print("Acetona: ",acetona_ppm)
        print("Tolueno: ",tolueno_ppm)
        print("Alcohol: ",alcohol_ppm)
        print("Humedad: ", humedad)

        vel_dif['x'] = vel_aux['x'] - vel['x']
        vel_dif['y'] = vel_aux['y'] - vel['y']
        vel_dif['z'] = vel_aux['z'] - vel['z']
        a_dif['x'] = a_bef['x'] - a_act['x']
        a_dif['y'] = a_bef['y'] - a_act['y']
        a_dif['z'] = a_bef['z'] - a_act['z']

        print("Temperatura : ",temperatura)
        print("Presion : ",presion,"(Pa)")
       
        dataXBEE = str(position['x']) + "," + str(position['y']) + "," + str(position['z'])  + ","
        dataXBEE = dataXBEE + str(vel['x']) + "," + str(vel['y']) + "," + str(vel['z']) + ","
        dataXBEE = dataXBEE + str(acc['x']) + "," + str(acc['y']) + "," + str(acc['z']) + ","
        dataXBEE = dataXBEE + str(temperatura) + "," + str(presion) + "," + str(humedad) + ","
        dataXBEE = dataXBEE + str(co_ppm) + "," + str(gpl_ppm) + "," + str(acetona_ppm) + "," 
        dataXBEE = dataXBEE + str(tolueno_ppm) + "," + str(alcohol_ppm) + "|"
        
        ledInterno.value(0)
        uart.write(dataXBEE)
        
        if vel_dif['x'] < -3 or vel_dif['x'] > 3:
            if vel['x'] < 0:
                position['x'] = xo - vel['x']*0.05 - (0.5*acc['x']*0.0025)
                xo = position['x']
            else:
                position['x'] = xo + vel['x']*0.05 + (0.5*acc['x']*0.0025)
                xo = position['x']
        if vel_dif['y'] < -6 or vel_dif['y'] > 6:
            # Gira derecha
            if vel['z'] < 0:
                if vel['y'] > 0:
                    position['y'] = yo - vel['y']*0.05 - (0.5*acc['y']*0.0025)
                    yo = position['y']
                else:
                    position['y'] = yo + vel['y']*0.05 + (0.5*acc['y']*0.0025)
                    yo = position['y']
            # Gira izquierda
            if vel['z'] > 0:
                if vel['y'] < 0:
                    position['y'] = yo - vel['y']*0.05 - (0.5*acc['y']*0.0025)
                    yo = position['y']
                else:
                    position['y'] = yo + vel['y']*0.05 + (0.5*acc['y']*0.0025)
                    yo = position['y']
        if a_act['z'] < 75:
            if a_act['x'] < 0:
                # mirando abajo
                if vel['z'] < 0:
                    position['z'] = zo + vel['z']*0.05 + (0.5*acc['z']*0.0025)
                    zo = position['z']
                else:
                    position['z'] = zo - vel['z']*0.05- (0.5*acc['z']*0.0025)
                    zo = position['z']
            else:
                # mirando arriba
                if vel['z'] < 0:
                    position['z'] = zo - vel['z']*0.05 - (0.5*acc['z']*0.0025)
                    zo = position['z']
                else:
                    position['z'] = zo + vel['z']*0.05 + (0.5*acc['z']*0.0025)
                    zo = position['z']
        print("----------------")
        #a_bef = a
        time.sleep(0.4)
    except (ZeroDivisionError):
        print("No división entre 0")
        
