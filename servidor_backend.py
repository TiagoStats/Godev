from model import Pessoa, SalaDeCafe, Sala
from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)

@app.route("/")
def inicio():
    return 'Sistema de cadastro de pessoas. <br>'+\
        '<a href="/listar_pessoas">Operação listar pessoas cadastradas!</a><br>'+\
        '<a href="/listar_salas">Operação listar salas cadastradas!</a><br>'

@app.route("/cadastrar_pessoa", methods=['post'])
def incluir_pessoa():
    dados = request.get_json(force=True)
    # obter os dados enviados pelo frontend
    nome = dados['nome']
    sobrenome = dados['sobrenome']
    # criar a nova pessoa
    Pessoa.create(nome=nome, sobrenome=sobrenome)
    print(nome)

@app.route("/cadastrar_sala", methods=['post'])
def incluir_sala():
    dados = request.get_json(force=True)
    # obter os dados enviados pelo frontend
    nome = dados['nome']
    lotacao_maxima = dados['lotacao_maxima']
    
    # criar a nova pessoa
    Sala.create(nome=nome, lotacao_maxima=lotacao_maxima, pessoas_na_sala = "")
    return(nome)

@app.route("/cadastrar_cafeteria", methods=['post'])
def incluir_cafeteria():
    dados = request.get_json(force=True)
    nome = dados['nome']
    SalaDeCafe.create(nome=nome, pessoas_na_sala = "")

@app.route("/listar_salas_primeiro_periodo")
def listar_salas():
    #Consultando os dados das pessoas e das salas cadastradas no banco de dados
    pessoas = list(map(model_to_dict, Pessoa.select()))
    dados_salas = list(map(model_to_dict, Sala.select()))
    lista_de_salas =[]
    numero_pessoas = [pessoas]
    
    #limpando dados de alunos em cada sala e iniciando uma lista com o numero de elementos igual ao número de salas cadastradas
    for i in range (len(dados_salas)):
        sala_a_receber_pessoa = Sala.get_by_id(i+1)
        sala_a_receber_pessoa.pessoas_na_sala = []
        sala_a_receber_pessoa.save()
        lista_de_salas.append(0)

    #comparando número de pessoas associadas a cada sala e encaminhando as mesmas para as salas adequadas (com número de pessoas menor)
    for i in range (len(numero_pessoas[0])):
        sala_com_menor_numero_de_pessoas = min(lista_de_salas)
        sala_com_mais_pessoas = max(lista_de_salas)
        if max(lista_de_salas) == 0:
            posicao_na_lista = lista_de_salas.index(max(lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(posicao_na_lista+1)
            sala_a_receber_pessoa.pessoas_na_sala =  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            lista_de_salas[posicao_na_lista] += 1
        
        elif min(lista_de_salas) == 0:
            posicao_na_lista = lista_de_salas.index(min(lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(posicao_na_lista+1)
            sala_a_receber_pessoa.pessoas_na_sala =  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            lista_de_salas[posicao_na_lista] += 1

        elif sala_com_mais_pessoas == sala_com_menor_numero_de_pessoas:
            sala_com_menos_pessoas = lista_de_salas.index(min(lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
            sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            lista_de_salas[sala_com_menos_pessoas] += 1

        else:
            sala_com_menos_pessoas = lista_de_salas.index(min(lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
            sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            lista_de_salas[sala_com_menos_pessoas] += 1
            
    #consultando novamente todos os dados das salas e enviando para o frontend 
    salas = list(map(model_to_dict, Sala.select()))
    return jsonify({'lista':salas})

@app.route("/listar_salas_segundo_periodo")
def listar_salas_segundo_periodo():
    #Consultando os dados das pessoas e das salas cadastradas no banco de dados
    pessoas = list(map(model_to_dict, Pessoa.select()))
    dados_salas = list(map(model_to_dict, Sala.select()))
    primeira_lista_de_salas = []
    lista_de_salas = []
    numero_pessoas = [pessoas]
    
    #limpando dados de alunos em cada sala e iniciando uma lista com o numero de elementos igual ao número de salas cadastradas
    for i in range (len(dados_salas)):
        sala_a_receber_pessoa = Sala.get_by_id(i+1)
        sala_a_receber_pessoa.pessoas_na_sala = []
        sala_a_receber_pessoa.save()
        primeira_lista_de_salas.append(0)

    for i in range (len(dados_salas)):
        sala_a_receber_pessoa = Sala.get_by_id(i+1)
        sala_a_receber_pessoa.pessoas_na_sala = []
        sala_a_receber_pessoa.save()
        lista_de_salas.append(0)

    #comparando número de pessoas associadas a cada sala e encaminhando aprimeira metade do total de pessoas para as salas adequadas (com número de pessoas menor)
    for i in range (len(numero_pessoas[0])//2):
        sala_com_menor_numero_de_pessoas = min(primeira_lista_de_salas)
        sala_com_mais_pessoas = max(primeira_lista_de_salas)
        if max(primeira_lista_de_salas) == 0:
            posicao_na_lista = primeira_lista_de_salas.index(max(primeira_lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(posicao_na_lista+1)
            sala_a_receber_pessoa.pessoas_na_sala =  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            primeira_lista_de_salas[posicao_na_lista] += 1
        
        elif min(primeira_lista_de_salas) == 0:
            posicao_na_lista = primeira_lista_de_salas.index(min(primeira_lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(posicao_na_lista+1)
            sala_a_receber_pessoa.pessoas_na_sala =  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            primeira_lista_de_salas[posicao_na_lista] += 1

        elif sala_com_mais_pessoas == sala_com_menor_numero_de_pessoas:
            sala_com_menos_pessoas = primeira_lista_de_salas.index(min(primeira_lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
            sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            primeira_lista_de_salas[sala_com_menos_pessoas] += 1

        else:
            sala_com_menos_pessoas = primeira_lista_de_salas.index(min(primeira_lista_de_salas))
            sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
            sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            sala_a_receber_pessoa.save()
            primeira_lista_de_salas[sala_com_menos_pessoas] += 1

    for i in range ((len(numero_pessoas[0])//2),len(numero_pessoas[0])): #pegando o indice certo
        sala_com_menor_numero_de_pessoas = min(primeira_lista_de_salas)
        sala_com_mais_pessoas = max(primeira_lista_de_salas)

        
        if sala_com_mais_pessoas == sala_com_menor_numero_de_pessoas:
            sala_com_menos_pessoas = primeira_lista_de_salas.index(min(primeira_lista_de_salas))
            if sala_com_menos_pessoas == len(primeira_lista_de_salas):
                segunda_sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
                segunda_sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
                segunda_sala_a_receber_pessoa.save()
                primeira_lista_de_salas[0] += 1
                print(primeira_lista_de_salas)  
                print("if 1")
            else:
                segunda_sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+2)
                segunda_sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
                segunda_sala_a_receber_pessoa.save()
                primeira_lista_de_salas[0] += 1
                print(primeira_lista_de_salas)  
                print("else 1")
            
            

        else:
            sala_com_menos_pessoas = primeira_lista_de_salas.index(min(primeira_lista_de_salas))
            if sala_com_menos_pessoas == len(primeira_lista_de_salas):
                segunda_sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
                segunda_sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
                segunda_sala_a_receber_pessoa.save()
                primeira_lista_de_salas[0] += 1
                print(primeira_lista_de_salas)
                print("if 2")

            elif  sala_com_menos_pessoas == 0:
                segunda_sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+3)
                segunda_sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
                segunda_sala_a_receber_pessoa.save()
                primeira_lista_de_salas[sala_com_menos_pessoas] += 1
                print(primeira_lista_de_salas)
                print("else 2")

            else:
                segunda_sala_a_receber_pessoa = Sala.get_by_id(sala_com_menos_pessoas+1)
                segunda_sala_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
                segunda_sala_a_receber_pessoa.save()
                primeira_lista_de_salas[sala_com_menos_pessoas] += 1
                print(primeira_lista_de_salas)
                print("else 2")
            
            
            
    #consultando novamente todos os dados das salas e enviando para o frontend 
    salas = list(map(model_to_dict, Sala.select()))
    return jsonify({'lista':salas})

@app.route("/listar_pessoas")
def listar_pessoas():
    pessoas = list(map(model_to_dict, Pessoa.select()))
    return jsonify({'lista':pessoas})

@app.route("/listar_cafeterias")
def listar_cafeterias():

    #Consultando os dados das pessoas e das salas cadastradas no banco de dados
    pessoas = list(map(model_to_dict, Pessoa.select()))
    dados_cafeterias = list(map(model_to_dict, SalaDeCafe.select()))
    lista_de_cafeterias =[]
    numero_pessoas = [pessoas]
    
    #limpando dados de alunos em cada sala e iniciando uma lista com o numero de elementos igual ao número de salas cadastradas
    for i in range (len(dados_cafeterias)):
        cafeteria_a_receber_pessoa = SalaDeCafe.get_by_id(i+1)
        cafeteria_a_receber_pessoa.pessoas_na_sala = []
        cafeteria_a_receber_pessoa.save()
        lista_de_cafeterias.append(0)

    #comparando número de pessoas associadas a cada cafeteria e encaminhando as mesmas para a cafeteria adequada (com número de pessoas menor)
    for i in range (len(numero_pessoas[0])):
        sala_com_menor_numero_de_pessoas = min(lista_de_cafeterias)
        sala_com_mais_pessoas = max(lista_de_cafeterias)
        if max(lista_de_cafeterias) == 0:
            posicao_na_lista = lista_de_cafeterias.index(max(lista_de_cafeterias))
            cafeteria_a_receber_pessoa = SalaDeCafe.get_by_id(posicao_na_lista+1)
            cafeteria_a_receber_pessoa.pessoas_na_sala =  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            cafeteria_a_receber_pessoa.save()
            lista_de_cafeterias[posicao_na_lista] += 1
        
        elif min(lista_de_cafeterias) == 0:
            posicao_na_lista = lista_de_cafeterias.index(min(lista_de_cafeterias))
            cafeteria_a_receber_pessoa = SalaDeCafe.get_by_id(posicao_na_lista+1)
            cafeteria_a_receber_pessoa.pessoas_na_sala =  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            cafeteria_a_receber_pessoa.save()
            lista_de_cafeterias[posicao_na_lista] += 1

        elif sala_com_mais_pessoas == sala_com_menor_numero_de_pessoas:
            sala_com_menos_pessoas = lista_de_cafeterias.index(min(lista_de_cafeterias))
            cafeteria_a_receber_pessoa = SalaDeCafe.get_by_id(sala_com_menos_pessoas+1)
            cafeteria_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            cafeteria_a_receber_pessoa.save()
            lista_de_cafeterias[sala_com_menos_pessoas] += 1

        else:
            sala_com_menos_pessoas = lista_de_cafeterias.index(min(lista_de_cafeterias))
            cafeteria_a_receber_pessoa = SalaDeCafe.get_by_id(sala_com_menos_pessoas+1)
            cafeteria_a_receber_pessoa.pessoas_na_sala +=  pessoas[i]["nome"] +" " + pessoas[i]["sobrenome"]+" | "
            cafeteria_a_receber_pessoa.save()
            lista_de_cafeterias[sala_com_menos_pessoas] += 1

        


    cafeterias = list(map(model_to_dict, SalaDeCafe.select()))
    return jsonify({'lista':cafeterias})

app.run(debug=True)