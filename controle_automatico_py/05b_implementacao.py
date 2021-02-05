from extra.aula import rodar

@rodar
def programa():
  
  # importação de bibliotecas
  from time import sleep
  from gpiozero import LED
  from pymongo import MongoClient, ASCENDING, DESCENDING
  from time import sleep
  from datetime import datetime
  from flask import Flask
  from requests import get
  
  # inicialização do banco e da chave do IFTTT
  cliente = MongoClient("localhost", 27017)
  banco = cliente["projeto5"]
  colecao = banco["estado_led"]
  app = Flask(__name__)
  
  
  # definição das funções
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
  
  @app.route("/led/<int:indice>/<string:estado>")
  def mostrar_leds(indice, estado):
    if estado == "on":
      atualiza_led(indice, True)
    elif estado == "off":
      atualiza_led(indice, False)
    return "Led " + str(indice) + " " + str(estado)
    
  
  # criação de componentes
  leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
  
  

  # criação do servidor
  app.run(port=5000, debug=False)

  

  # definição das páginas do servidor
  
  
    
  # rode o servidor
  
  atualiza_led(3, False)
  
  # loop infinito (pode remover depois de criar o servidor)
  while True:

    sleep(0.2)
  
    
