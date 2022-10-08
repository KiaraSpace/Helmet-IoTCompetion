# calculos_gas.py
import math

class Calculos:
    '''Tiene los métodos necesarios para calculas las
    PPM de cualquier sensor MQ'''

    @classmethod
    def calcular_voltaje(cls, ADC, factor):
        ''' Calcula el voltaje de media leido en un intervalo de tiempo'''
        voltaje = ADC*factor
        return voltaje

    @classmethod
    def calcular_resistencia(cls, voltaje, resistencia):
        '''Con el voltaje y la resistencia del PCB del sensor podemos calcular
        la resistentencia que te tendrá el sensor. Esta resistencia se
        representa como Rs.'''
        resultado = 0
        if (voltaje != 0):
            resultado = float(
                resistencia * (4.9 - float(voltaje)) / float(voltaje))
        return resultado

    @classmethod
    def calcular_ppm(cls, ratio, curva_gas):
        '''Mediante calculos logaritmicos nos devuelve los ppm de un gas
        en particular.'''

        concentracion = math.pow(
            10,
            ((math.log(ratio) - curva_gas[1]) / curva_gas[2]) + curva_gas[0]
        )
        return str(round(concentracion, 3))

