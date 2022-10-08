# IoT CHAMPIONS

# Presentación

El objetivo del presente proyecto es el de otorgar un grado mayor de seguridad a los trabajadores mineros, al mismo tiempo que el de brindar mayor información en tiempo real a los operarios mineros que se encuentran fuera de la mina monitoreando el avance en esta; esto se lograría mediante el monitoreo constante de dos variables fundamentales, estas son: la localización del trabajador dentro de la mina, la calidad del aire en el lugar exacto en el que se encuentra el trabajador.

-----------------------------------------------------------------------------------------------------------------------------------------------
## Información del grupo

1. Nombre de los integrantes:

    * Echevarria Duran, Patrick Fabrizio
    * Quispe Cardenas, Paulo Roberto
    * Sare Vargas, Nilton Sare
    * Montoya Obeso, Leonardo
    * Rodriguez Bautista, Kiara Micaela 
----------------------------------------------------------------------------------------------------------------------------------------------------

# Arquitectura de la Solución:
![Arquitectura](https://user-images.githubusercontent.com/86942136/194683226-343cbc14-5698-4fa0-af80-2e311c37f7b3.png)

----------------------------------------------------------------------------------------------------------------------------------------------------

# Diseño de prototipo:
![casco](https://user-images.githubusercontent.com/80610961/194684288-1041d4ea-b8a7-4bdf-a154-f7bc14a471de.png)


----------------------------------------------------------------------------------------------------------------------------------------------------

# Prototipo:

![image](https://user-images.githubusercontent.com/80610961/194684693-de48592a-9e6e-4ec0-8409-808e9ea6ae96.png)

En el área de hardware, el prototipo planteado consta de una Raspberry Pi Pico como computador central, el cual recopilará la data de una variedad de sensores, los cuales nos brindarán un monitoreo completo del minero en su área de trabajo. Los sensores utilizados son:

* MQ-09
* MQ-135
* BMP280
* DHT11
* MPU9250

## Hardware del prototipo implementado:
![image](https://user-images.githubusercontent.com/80610961/194448796-8b77bc99-e6ff-47a9-adc3-0892a6a0e1ed.png)

![image](https://user-images.githubusercontent.com/80610961/194448818-232eac5b-d3b1-4b01-b68a-59f5ee1d9486.png)

## Dashboard de visualización de datos obtenidos en tiempo real:
Los datos obtenidos de los sensores se visualizarán en la plataforma diseñada en Node-red.    

![image](https://user-images.githubusercontent.com/80610961/194457489-41371f54-afdc-47ae-afbb-62f78dc6dde2.png)

Link del Dashboard
http://18.229.159.18:1880/ui

Agregar que se adiciono seguridad al Backend de Node-red
![image](https://user-images.githubusercontent.com/86942136/194724887-2b6d547c-a119-4c75-a127-fa1880fdbd74.png)

## Código- Software:
1. El código `Concurso IOT.json`, consta de la implementación general de los dashboards de visualización de datos en tiempo real en Node-Red.
2. El código `Code.py`, consta de la programación de todos los sensores, además del algoritmo de localización.
