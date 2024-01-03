import machine
import utime

trig1 = machine.Pin(1, machine.Pin.OUT)
echo1 = machine.Pin(0, machine.Pin.IN)
trig2 = machine.Pin(13, machine.Pin.OUT)
echo2 = machine.Pin(14, machine.Pin.IN)
avanzar = machine.Pin(5, machine.Pin.OUT)
retroceder = machine.Pin(6, machine.Pin.OUT)
buzzer = machine.Pin(15, machine.Pin.OUT)
utime.sleep(2)

# Inicialmente, el carrito se moverá hacia adelante.
direccion_mov = False
avanzar.on()
retroceder.off()

def medir_distancia(trig, echo):
    trig.on()
    utime.sleep_us(10)
    trig.off()
    
    while echo.value() == 0:
        pulso_inicio = utime.ticks_us()

    while echo.value() == 1:
        pulso_fin = utime.ticks_us()

    duracion = utime.ticks_diff(pulso_fin, pulso_inicio)
    distancia = (duracion / 2) * 0.0343

    return distancia

while True:
    distancia_frontal = medir_distancia(trig1, echo1)
    distancia_trasera = medir_distancia(trig2, echo2)
    direccion_mov_anterior = direccion_mov

    #print("Distancia frontal:", distancia_frontal, "cm")
    #print("Distancia trasera:", distancia_trasera, "cm")

    if ((distancia_frontal < 10) and (distancia_trasera < 10)):
        avanzar.off()
        retroceder.off() #perfeccionar esto
        buzzer.on()
    
    if ((distancia_izquierda > 10) and (distancia_derecha > 10)):
        buzzer.off()
        
    if distancia_frontal < 10:
        direccion_mov = True
        buzzer.on()
 
    if distancia_trasera < 10:
        direccion_mov = False
        buzzer.on()

        
    if ((direccion_mov == True) and (direccion_mov_anterior == False)):
        avanzar.off()
        retroceder.on()
        
    if ((direccion_mov == False) and (direccion_mov_anterior == True)):
        retroceder.off()
        avanzar.on()
    #print(direccion_mov)
    utime.sleep_ms(200)