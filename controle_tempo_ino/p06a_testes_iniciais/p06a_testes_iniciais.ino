  #define USE_TIMER_1 true

  #include <ShiftDisplay.h>
  #include<TimerInterrupt.h>
  #include<GFButton.h>


  int led = 13,led2 = 12;
  bool estadoled2 = false;
  ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
  GFButton botao2(A2);
  GFButton botao3(A3);
  int count = 0;

  void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(led, OUTPUT);
    pinMode(led2, OUTPUT);
    digitalWrite(led, HIGH);
    display.set(-4.12, 2);
    display.show(2000);
    botao2.setPressHandler(muda_botao2);
    botao3.setPressHandler(pressiona_botao3);
    ITimer1.init();
    ITimer1.attachInterruptInterval(2000, imprime_contador);
  }


  void loop() {
    // put your main code here, to run repeatedly:
    digitalWrite(led, LOW);
    botao2.process();
    botao3.process();
    display.set(count);
    display.update();
  }

  void muda_botao2(GFButton& botao2){

    if (estadoled2){
      digitalWrite(led2,HIGH);
      estadoled2 = false;
    }
    else {
      digitalWrite(led2,LOW);
      estadoled2 = true;
    }
    
  }
  
  void imprime_contador(){
    Serial.println(count);
  }

  void pressiona_botao3(GFButton& botao3) {
    count++;
  }
