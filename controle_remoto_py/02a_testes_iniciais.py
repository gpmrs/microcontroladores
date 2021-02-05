from extra.aula import rodar

@rodar
def programa():
    
  # importação de bibliotecas
  from gpiozero import LED
  from time import sleep
  from gpiozero import Button
  from Adafruit_CharLCD import Adafruit_CharLCD
  from lirc import init, nextcode
  from py_irsend.irsend import send_once 



  # definição de funções
  def acende_todos():
    for led in leds:
      led.on()


  def apaga_todos():
    for led in leds:
      led.off()
  
  # criação de componentes
  leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
  botao1 = Button(11)
  botao2 = Button(12)
  lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)
  botao1.when_pressed = acende_todos
  botao2.when_pressed = apaga_todos
  receptor = init("aula", blocking=False)
  select = 1

  # loop infinito
  while True:
    lista_com_codigo = nextcode()
    if lista_com_codigo != []:
      codigo = lista_com_codigo[0]
      if codigo == "KEY_1":
        select = 1
        lcd.clear()
        lcd.message("tecla 1\nselecionada")
      elif codigo == "KEY_2":
        select = 2
        lcd.clear()
        lcd.message("tecla 2\nselecionada")
      elif codigo == "KEY_3":
        select = 3
        lcd.clear()
        lcd.message("tecla 3\nselecionada")
      elif codigo == "KEY_4":
        select = 4
        lcd.clear()
        lcd.message("tecla 4\nselecionada")
      elif codigo == "KEY_5":
        select = 5
        lcd.clear()
        lcd.message("tecla %s \nselecionada" % select)
      elif codigo == "KEY_UP":
        if select == 1:
          select = 1
        else:
          select -= 1
        lcd.clear()
        lcd.message("tecla %s \nselecionada" % select)
      elif codigo == "KEY_DOWN":
        if select == 5:
          select = 5
        else:
          select += 1
        lcd.clear()
        lcd.message("tecla %s \nselecionada" % select)
      elif codigo == "KEY_OK" and select != 0:
        leds[select-1].toggle()
    
    sleep(0.2)
