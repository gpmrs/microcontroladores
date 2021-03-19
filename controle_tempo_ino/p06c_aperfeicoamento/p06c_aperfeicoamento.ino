// COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO

#define USE_TIMER_1 true

#include <ShiftDisplay.h>
#include<TimerInterrupt.h>
#include<GFButton.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
int t[] = {0, 0, 0, 0};
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
bool em_andamento[] = {false, false, false, false};
int campainha = 3;
int indice = 0;
int leds[] = {13, 12, 11, 10};

void setup() {
  Serial.begin(9600);
  pinMode(leds[0], OUTPUT);
  pinMode(leds[1], OUTPUT);
  pinMode(leds[2], OUTPUT);
  pinMode(leds[3], OUTPUT);
  digitalWrite(leds[0], LOW);
  digitalWrite(leds[1], HIGH);
  digitalWrite(leds[2], HIGH);
  digitalWrite(leds[3], HIGH);
  ITimer1.init();
  ITimer1.attachInterruptInterval(1000, verifica_andamento);
  botao1.setPressHandler(acrescenta_15);
  botao2.setPressHandler(diminui_15);
  botao3.setPressHandler(muda_andamento);
  pinMode(campainha, OUTPUT);
  digitalWrite(campainha, HIGH);
}

void termina_contagem(int posicao){
  em_andamento[posicao] = false;
  digitalWrite(campainha,LOW);
  delay(500);
  digitalWrite(campainha,HIGH);
  t[posicao] = 0;
  digitalWrite(leds[posicao], HIGH);
}

void loop() {
  int tempo = 100*(t[indice]/60) +t[indice]%60;
  display.set(tempo, 0, 3);
  display.changeDot(1, true);
  display.update();
  botao1.process();
  botao2.process();
  botao3.process();
  for (int i =0;i<4;i++){
    if (t[i] == 0 && em_andamento[i]){
     termina_contagem(i);
    }
  }

}

void verifica_andamento(){
for (int i =0;i < 4; i++){
   if (em_andamento[i]){
    t[i]--;
   }
 }
}

void muda_andamento(){
  if (em_andamento[indice] || t[indice]==0){
    if (indice <3){
      digitalWrite(leds[indice],HIGH);
      indice ++;
      digitalWrite(leds[indice],LOW);
    }
    else{
      digitalWrite(leds[indice],HIGH);
      indice = 0;
      digitalWrite(leds[indice], LOW);
    }
  }
  else {
    em_andamento[indice] = true;
  }
}

void acrescenta_15() {
  t[indice] = t[indice] + 15;
}

void diminui_15() {
  if (t[indice] < 15) {
    t[indice] = 0;
  }
  else {
    t[indice] = t[indice] - 15;
  }
}

// DEPOIS FAÇA OS NOVOS RECURSOS
