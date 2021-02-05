from extra.aula import rodar

@rodar
def programa():
    
  # importação de bibliotecas
  from gpiozero import LED
  from time import sleep


  # definição de funções
  

  # criação de componentes
  leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
  

  # loop infinito
  while True:

    sleep(0.2)
