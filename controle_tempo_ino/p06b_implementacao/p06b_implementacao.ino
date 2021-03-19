#include <AFMotor.h>

#define VELOCIDADE 160

AF_DCMotor motorA(3);
AF_DCMotor motorB(4);

int sensorOtico = A11;
int sensorOtico2 = A12;

unsigned long instanteAnteriorDeDeteccao = 0;

void setup() {
  Serial.begin(9600);
  pinMode(sensorOtico, INPUT);
  pinMode(sensorOtico2, INPUT);
  motorA.setSpeed(VELOCIDADE);
  motorB.setSpeed(VELOCIDADE);
     
}

void loop() {

  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    // remove quebra de linha
    if (texto.startsWith("frente")) {
      frente();
    }
    else if(texto.startsWith("tras")){
      tras();
    }
    else if(texto.startsWith("esquerda")){
      esquerda();
    }
    else if(texto.startsWith("direita")){
      direita();
    }
    else if(texto.startsWith("parar")){
      parar();
    }
  }
  
  if (millis() > instanteAnteriorDeDeteccao + 100) {
    int valorAnalogico = analogRead(sensorOtico);
    int valorAnalogico2 = analogRead(sensorOtico2);
    Serial.println(valorAnalogico);
    Serial.println("-");
    Serial.println(valorAnalogico2);
    instanteAnteriorDeDeteccao = millis();
  }
}


void frente()
{

  motorA.run(FORWARD);

  motorB.run(FORWARD);
  
}

void tras()
{

  motorA.run(BACKWARD);

  motorB.run(BACKWARD);
  
}

void direita()
{

  motorA.run(FORWARD);
  
  motorB.run(RELEASE);
  
}

void esquerda()
{

  motorA.run(RELEASE);

  motorB.run(FORWARD);
  
}

void parar()
{

  motorA.run(RELEASE);

  motorB.run(RELEASE);
  
}
