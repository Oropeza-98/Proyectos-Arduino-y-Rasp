from machine import Pin, I2C
from time import sleep
from pico_i2c_lcd import I2cLcd

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c,39,2,16)
TECLA_ARRIBA = const(0)
TECLA_ABAJO = const(1)
ACTIVADO = const(1)
#esta mal decir planetas a la lista por que esta el sol, pero ya me fastidie jajaja

aceleraciones_planetas = [
    273.7,  # Aceleración de la gravedad en el Sol (m/s^2)
    3.7,    # Aceleración de la gravedad en Mercurio (m/s^2)
    8.87,   # Aceleración de la gravedad en Venus (m/s^2)
    9.81,   # Aceleración de la gravedad en la Tierra (m/s^2)
    3.71,   # Aceleración de la gravedad en Marte (m/s^2)
    24.79,  # Aceleración de la gravedad en Júpiter (m/s^2)
    10.44,  # Aceleración de la gravedad en Saturno (m/s^2)
    8.69,   # Aceleración de la gravedad en Urano (m/s^2)
    11.15,  # Aceleración de la gravedad en Neptuno (m/s^2)
    1.62    # Aceleración de la gravedad en Neptuno (m/s^2)
    
]
planetas = ["Sol", "Mercurio", "Venus", "Tierra", "Marte",
            "Jupiter", "Saturno", "Urano", "Neptuno", "Luna"]


def peso(masa, aceleracion):
    peso_calc = round(float(masa) * aceleracion, 2)
    return peso_calc

teclas = [['1', '2', '3', 'A'],
          ['4', '5', '6', '10'],
          ['7', '8', '9', '11'],
          ['.', '0', '#', 'D']]

pines = list(range(2,10))
filas = pines[:4]
columnas = pines[4:]

#definir objetos para filas y columnas

fila_pines = [Pin(nombre_pin, mode=Pin.OUT) for nombre_pin in filas]

columna_pines = [Pin(nombre_pin, mode=Pin.IN, pull=Pin.PULL_DOWN) for nombre_pin in columnas]

def init():
    for fila in range(0, 4):
        for columna in range(0,4):
            fila_pines[fila].low()

def scan(fila, columna):
    fila_pines[fila].high()
    tecla = None
    
    if columna_pines[columna].value() == TECLA_ABAJO:
        tecla = TECLA_ABAJO
    if columna_pines[columna].value() == TECLA_ARRIBA:
        tecla = TECLA_ARRIBA        
    
    fila_pines[fila].low()
    return tecla
    



while True:
    numeros_teclado = ['.','0','1','2','3','4','5','6','7','8','9']
    numeros_tec = ['0','1','2','3','4','5','6','7','8','9', ]
    print("Listo prueba")
    lcd.putstr("INGRESA TU MASA EN LA TIERRA(Kg)")
    tecla_presionada = None
    x = None
    masa = ""
    masap = ""
    init()
    
    salir = False
    salir2 = False
    
    while not salir:
        for fila in range(4):
            for columna in range(4):
                tecla = scan(fila, columna)
                
                if tecla == TECLA_ABAJO:
                    print("Tecla Presionada", teclas[fila][columna])
                    sleep(0.5)  # Esperar 0.5 segundos antes de continuar
                    tecla_anterior = tecla_presionada
                    tecla_presionada = teclas[fila][columna]
                
                    if ((tecla_presionada in numeros_teclado) and (tecla_anterior is None)):
                        lcd.clear()

                    if tecla_presionada in numeros_teclado:
                        print("{} guardado".format(tecla_presionada))
                        #lcd.clear()
                        masa += tecla_presionada
                        masap += tecla_presionada +"kg"
                        sleep(0.5)
                        lcd.clear()
                        lcd.putstr(masap)
                        masap = masap[:-2]
                        
                    if tecla_presionada == '#':
                        lcd.clear()
                        lcd.putstr("Elige un planeta (D) Salir")
                        
                        while not salir2:
                            for fila in range(4):
                                for columna in range(4):
                                    tecla = scan(fila, columna)
                                    
                                    if tecla == TECLA_ABAJO:
                                        print("Tecla Presionada", teclas[fila][columna])
                                        sleep(0.5)  # Esperar 0.5 segundos antes de continuar
                                        x = teclas[fila][columna]
                                    

                                        if x in numeros_tec:
                                            print("{} guardado".format(int(x)))
                                            lcd.clear()
                                            aceleracion = aceleraciones_planetas[int(x)]
                                            pesoC = peso(masa, aceleracion)
                                            print(pesoC)
                                            lcd.putstr("Peso => " + planetas[int(x)])
                                            lcd.move_to(0,1)
                                            lcd.putstr(str(pesoC) + "Newtos")
                                            sleep(0.5)
                                            
                                    
                            
                                        if x == 'D':
                                            lcd.clear()
                                            salir2 = True
                                            salir = True
                                            break
                        
                    
                        
                    
                    if tecla_presionada == 'A':
                        masap = masap[:-1]
                        masa = masa[:-1]
                        lcd.clear()
                        print(masap + "kg")
                        lcd.putstr(masap + "Kg")
                        
                    if tecla_presionada == 'D':
                        lcd.clear()
                        salir = True
                        break