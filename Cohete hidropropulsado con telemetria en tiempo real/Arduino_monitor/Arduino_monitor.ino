//Librerias del sensor BMP280
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
//Librerias del modulo NRF24L01
#include <SPI.h>
#include <nRF24L01.h>
#include <printf.h>
#include <RF24.h>
#include <RF24_config.h>


const int CE=9;              //el pin 9 llama al modulo NRF24L01
const int CSN=10;            //EL pin 10 permite la comunicacion del arduino y el modulo NRF24L01
float a=0, b=0, altitudMaxRelativa = 0, altura=0;     
const uint64_t canal[2] = {0xE8E8F0E1LL,0xE8E8F0E2LL};  //canales de comunicacion del modulo NRF24L01
float lectura_datos[3];      //Declaramos como flotante una lista con espacios 0, 1, 2, 3
RF24 radio(CE, CSN);   //establecemos los canales que asignamos arriba




void setup() {
Serial.begin(9600);   //Iniciamos al funcion para que el monitor serial nos muestre la información
  radio.begin();   //Iniciamos la funcion para iniciar el modulo NRF24L01
  radio.setRetries(5,10);   //Establecemos; (numero de intentos de comunicacion, tiempo en ms que dura el intento)
  radio.openWritingPipe(canal[1]);   //Declaramos el canal 1 como canal de ESCRITURA para el modulo NRF24L01 (HABLAR)
  radio.openReadingPipe(0,canal[0]);   //Declaramos el canal 0 como canal de LECTRUA para el modulo NRF24L01 (ESCUCHAR)
  radio.setPALevel(RF24_PA_MAX);   //Establecemos el nivel maximo en la potencia del modulo NRF24L01
 
}

void loop() {
 //Receptor
radio.startListening();   //Iniciamos la recepcion de informacion en el modulo NRF24L01

if (lectura_datos[0]>a){   // preparamos la variable a para registrar la temperatura maxima
a=lectura_datos[0];
  }
/*if (lectura_datos[2]>b){   // preparamos la variable b para registrar la altura maxima
b=lectura_datos[2];
  }*/
//altitudMaxRelativa = b-1139.355;  //Con esta linea de codigo se calibran las lecturas modificando la condicion inicial para nuestra necesitad
altura = lectura_datos[2]+671;
if (altura>b){   // preparamos la variable b para registrar la altura maxima
b=altura;
  }
altitudMaxRelativa = b-1810.6;
if(radio.available())
  radio.read(&lectura_datos,sizeof(lectura_datos)); //Hacemos que el modulo NRF24L01 reciba la lista lectura_datos
  Serial.print("Temperatura: ");          //A partir de aquí es imprimir en el monitor serial la informacíon del sensor
  Serial.print(lectura_datos[0],4);
  Serial.print("C || ");
  Serial.print("Temperatura MAX: ");
  Serial.print(a, 4);
  Serial.print("C || ");
  Serial.print("Presion: ");
  Serial.print(lectura_datos[1],4);
  Serial.print("hPa || ");
  Serial.print("Altitud: ");
  Serial.print(altura,4);
  Serial.print("m || ");
  Serial.print("Altitud MAX: ");
  Serial.print(b, 4);
  Serial.print("m || ");
  Serial.print("Altitud MAXrel: ");
  Serial.print(altitudMaxRelativa, 4);
  Serial.print("m || ");
  Serial.println(); //Imprimimos un salto de linea
  //Serial.println(estado); 

  delay(1000);   //Retrasamos el loop 1 segundo

}
