from extra.aula import rodar

@rodar
def programa():
  
  # importação de bibliotecas
  from gpiozero import LED
  from time import sleep
  
  
  # definição de funções
  
  
  # criação de componentes
  led = LED(21)
  
  
  # loop infinito
  while True:
    
    sleep(0.2)
