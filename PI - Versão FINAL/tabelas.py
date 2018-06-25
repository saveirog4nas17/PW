from peewee import Model, CharField, ForeignKeyField
import json
from playhouse.shortcuts import model_to_dict
from peewee import SqliteDatabase
db = SqliteDatabase("bancodedados.db")

#from peewee import PostgresqlDatabase
#db = PostgresqlDatabase('teste', user='postgres', password='', host='192.168.99.100', port=5432)

                           
class BaseModel(Model):
    """Um modelo que serve de base para o banco de dados postgre."""
    class Meta:
        database = db
        
class Pessoa(BaseModel):
    usuario = CharField(unique=True)
    email = CharField(unique=True)
    senha = CharField()
    foto_url = CharField()
    frase = CharField()
    cidade = CharField()
    bairro = CharField()
    rua = CharField()
    numero = CharField()

class Cardapio(BaseModel):
    nome = CharField()

class Empresa(BaseModel):
    nome = CharField()
    cnpj = CharField(unique=True)
    foto_url = CharField()

    @staticmethod
    def lista():
        empresas = Empresa.select()
        empresas = [model_to_dict(e) for e in empresas]
        return empresas

    @staticmethod
    def listaJSON():
        empresas = Empresa.lista()
        return json.dumps(empresas)

class Produto(BaseModel):
    empresa = ForeignKeyField(Empresa, backref='produtos')
    categoria = CharField() 
    nome = CharField()
    valor = CharField()
    
class Pedidos(BaseModel):
   pessoa = ForeignKeyField(Pessoa, backref='pedidos')
   estadoPedido = CharField() # estados: pedindo, finalizado, entregando

   def qtd(self):
       
       return self.pedidosProdutos.count()
    
   
class PedidoProduto(BaseModel):
    produto = ForeignKeyField(Produto, backref='pedidosProdutos')
    pedido = ForeignKeyField(Pedidos, backref='pedidosProdutos')
    