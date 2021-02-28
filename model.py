from peewee import *

arq = 'bandodedados.db'
db = SqliteDatabase(arq)

class BaseModel(Model):
    class Meta:
        database = db

class Sala(BaseModel):
    nome = CharField()
    lotacao_maxima = CharField()
    pessoas_na_sala = CharField()


class Pessoa(BaseModel):
    nome = CharField()
    sobrenome = CharField()

class SalaDeCafe(BaseModel):
    nome = CharField()
    pessoas_na_sala = CharField()


if __name__ == "__main__":
    db.connect()
    db.create_tables([Sala, Pessoa, SalaDeCafe])
    #joao = Pessoa.create(nome="Joao", sobrenome="da Silva")
    #sala_01 = Sala.create(nome="Sala 01", lotacao_maxima="100", pessoas_na_sala = "")
    #print(joao.nome, ",", joao.sobrenome)
   # print(sala_01.pessoas_na_sala)