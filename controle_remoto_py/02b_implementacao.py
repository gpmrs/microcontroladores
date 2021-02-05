from extra.aula import rodar

@rodar
def programa():
  # importação de bibliotecas
  from flask import Flask
  from py_irsend.irsend import send_once
  from threading import Timer
  
    
  # criação do servidor
  app = Flask(__name__)
  
  # definição de funções das páginas
  @app.route("/")
  def inicio():
    return "Bem vindo!"

  @app.route("/power")
  def pag_power():
    send_once("aquario", ["KEY_POWER"])
    return "desligando a TV"

  @app.route("/aumenta")
  def pag_aumenta():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return " aumentando o volume"

  @app.route("/diminui")
  def pag_diminui():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return "diminuindo o volume"
    
  @app.route("/mudo")
  def pag_mudo():
    send_once("aquario", ["KEY_MUTE"])
    return "Som mudo"

  @app.route("/mudacanal/<string:canal_selecionado>")
  def pag_canal(canal_selecionado):
    for numero in canal_selecionado:
      send_once("aquario",["KEY_%s"%(numero)])
    return "Mudou o canal"
  
  @app.route("/timer/<int:tempo_off>")
  def pag_timer(tempo_off):
    t = Timer(tempo_off, pag_power)
    t.start()
    return "Desligando em %d segundos"%(tempo_off)  


  # rode o servidor
  app.run(port=5000, debug=False)
    
