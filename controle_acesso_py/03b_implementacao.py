from extra.aula import rodar

@rodar
def programa():
  # importação de bibliotecas
  from extra.redefinir_banco import redefinir_banco
  from pymongo import MongoClient
  from time import sleep
  
  # a linha abaixo apaga todo o banco e reinsere os moradores
  redefinir_banco()
  
  # parâmetros iniciais do banco
  cliente = MongoClient("localhost", 27017)
  banco = cliente["projeto03"]
  colecao = banco["moradores"]
  
  
  # definição de funções
  
  
  # criação de componentes
  
  
  # loop infinito
  while True:
    sleep(0.2)
    