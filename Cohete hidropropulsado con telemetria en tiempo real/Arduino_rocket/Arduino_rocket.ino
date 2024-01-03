//Librerias para el sensor BMP280
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
//Librerias para el modulo NRF24L01
#include <SPI.h>
#include <nRF24L01.h>
#include <printf.h>
#include <RF24.h>
#include <RF24_config.h>
#include <Servo.h>



Adafruit_BMP280 bmp;
const int CE=9;       //le asignamos el valor del pin 9 a CE
const int CSN=10;    //Le asignamos el valor del pin 10 a CSN
RF24 radio(CE, CSN);   //establecemos los canales que asignamos arriba
const uint64_t canal[2] = {0xE8E8F0E1LL,0xE8E8F0E2LL};   //canales para la comunicacion entre los modulos NRF24L01 
float presion, temperatura, p0, lectura_datos[3], altitud;   /*Declaramos como flotantes, presion, temperatura, p0 
                                                              y una lista con 4 espacios: 0, 1, 2, 3.*/
float c = 0;
int d = 0;
Servo motor;

void setup() {
 radio.begin();   //iniciamos la función radio para que empiece a transmitir informacion el modulo NRF24L01
 bmp.begin();   //iniciamos la funcion de lectura para el sensor BMP280
 radio.setRetries(5,10);   //Establecemos; (numero de intentos de comunicacion, tiempo en ms que dura el intento)
 radio.openWritingPipe(canal[0]);   //Declaramos el canal 0 como canal de ESCRITURA para el modulo NRF24L01 (HABLAR)
 radio.openReadingPipe(1,canal[1]);  //Declaramos el cnaal 1 como canal de LECTURA para el modulo NRF24L01  (ESCUCHAR)
 radio.setPALevel(RF24_PA_MAX);   //Establecemos el nivel maximo en la potencia del modulo NRF24L01
 p0 =(bmp.readPressure()/100)+189;  //Establecemos un valor inicial apra la presión
 motor.attach(6);
 motor.write(0);
}

void loop() {
  //EMISOR
  temperatura = bmp.readTemperature();   // Establecemos la lectura de la temperatura en el loop
  presion = (bmp.readPressure()/100)+189;  // Establecemos la lectura de la presión en el loop
  altitud = (bmp.readAltitude(p0))+69;   //Establecemos el calculo de la altitud
  lectura_datos[0]=temperatura;  // Almacenamos la lectura de la temperatura en el espacio 0 de lectura_datos
  lectura_datos[1]=presion;   //Almacenamos la lectura de la presión en el espacio 1 de lectura_datos
  lectura_datos[2]=altitud;   //Almacenamos el calculo de la altitud en el espacio 2 de lectura_datos
  radio.write(&lectura_datos, sizeof(lectura_datos));   //Enviamos lectura_datos a travez del modulo NRF24L01
  
  if (altitud > c){
    c = altitud;
  }
  d = c - altitud;
  if (d > 5){
    motor.write(140);
  }





  delay(1000);   //Rtrasamos el loop 1 segundo


}
