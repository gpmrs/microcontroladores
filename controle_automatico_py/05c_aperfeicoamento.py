from extra.aula import rodar

@rodar
def programa():
  
  # importação de bibliotecas
  from time import sleep
  from gpiozero import LightSensor, Button, MotionSensor, LED
  from pymongo import MongoClient, ASCENDING, DESCENDING
  from time import sleep
  from datetime import datetime
  from flask import Flask
  from requests import get
  from threading import Timer
  
  # inicialização do banco e da chave do IFTTT
  cliente = MongoClient("localhost", 27017)
  banco = cliente["projeto5"]
  colecao = banco["estado_led"]
  
  
 
  leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
  # definição das funções
  def parar_timer():
    global timer
    if timer != None:
      timer.cancel()
      timer = None
    
  def atualiza_led(indice, aceso):
    if aceso == False:
      leds[indice].off()
    elif aceso == True:
      leds[indice].on()

    estados=[]
    for led in leds:
      estados.append(led.is_lit)
    
    dados = {"data": datetime.now(), "estados": estados}
    colecao.insert(dados)

  def desliga_led1():
    atualiza_led(0, False)

  def movimento_detectado():
    
    parar_timer()
    atualiza_led(0, True)
  
  def sem_movimento():
    global timer
    timer =Timer(6, desliga_led1)
    timer.start()

  def acende_luz():
    atualiza_led(1, True)

  def apaga_luz():
    atualiza_led(1, False)


 
  # criação de componentes
  global timer
  timer = None
  
  sensor_de_movimento = MotionSensor(27)
  sensor_de_luz = LightSensor(8)
  
  
  sensor_de_movimento.when_motion = movimento_detectado
  sensor_de_movimento.when_no_motion = sem_movimento
  sensor_de_luz.when_dark = acende_luz
  sensor_de_luz.when_light = apaga_luz

  busca = {}
  ordenacao = [ ["data", DESCENDING] ]


  documento = colecao.find_one(busca, sort=ordenacao)
  
  if documento != None:
    for (i,estado) in enumerate(documento["estados"]):
      if estado == True:
        leds[i].on()
      else:
        leds[i].off()
  

  # criação do servidor
  app = Flask(__name__)

  # definição das páginas do servidor
  @app.route("/led/<int:indice>/<string:estado>")
  def mostrar_leds(indice, estado):
    if estado == "on":
      atualiza_led(indice, True)
    elif estado == "off":
      atualiza_led(indice, False)
    return "Led " + str(indice) + " " + str(estado)

  @app.route("/")
  def estado_atual():
    html = "<ul>"
    for (i,led) in enumerate(leds):
      html+="<li>Luz %d: "%(i+1)
      if led.is_lit:
        html+= "aceso"
      else:
        html+= "apagado"
      html+="</li>"
    html+="</ul>"
    return html
  
  
    
  # rode o servidor
  app.run(port=5000, debug=False)
  
  # loop infinito (pode remover depois de criar o servidor)
  while True:

    sleep(0.2)
  
    
