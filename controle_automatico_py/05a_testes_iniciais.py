from extra.aula import rodar

@rodar
def programa():
    
  # importação de bibliotecas
  from time import sleep
  from threading import Timer
  from requests import post
  from gpiozero import LightSensor, Button, MotionSensor, LED, DistanceSensor
  

  # definição de funções  
  def movimento_detectado():
    parar_timer()
    led_1.on()
    led_2.on()
    
    
  def sem_movimento():
    led_1.off()
    global timer
    timer =Timer(4, desliga_led2)
    timer.start()

  def desliga_led2():
    led_2.off()

  def parar_timer():
    global timer
    if timer != None:
      timer.cancel()
      timer = None
    

  def mov_detectado():
    movimento_detectado()
    
  def botao_pressionado():
    dados = {"value1": sensor_de_luz.value*100, "value2": sensor_de_distancia.distance*100}
    resultado = post(endereco1, json=dados)
    print(resultado.text)




  # criação de componentes
  global timer
  timer = None
  sensor_de_movimento = MotionSensor(27)
  sensor_de_distancia = DistanceSensor(trigger=17, echo=18)
  chave1 = "d1NVosCimwDS5artn4kGbt"
  chave2 = "diVRG6YTEu2qM8h7po2d4"
  evento = "botao_pressionado"
  
  endereco1 = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave1
  endereco2 = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave2
   
  

  led_1 = LED(21)
  led_2 = LED(22)
  botao = Button(11)
  sensor_de_luz = LightSensor(8) 
  


  sensor_de_movimento.when_motion = mov_detectado
  sensor_de_movimento.when_no_motion = sem_movimento
  botao.when_pressed = botao_pressionado

  


 

  # loop infinito
  while True:


    sleep(0.2)
