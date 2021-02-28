from flask import Flask, render_template, request, redirect, jsonify, json
from model import Pessoa, Sala, SalaDeCafe
import requests
from playhouse.shortcuts import dict_to_model

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/listar_pessoas")
def listar_pessoas():
    dados_pessoas = requests.get('http://localhost:5000/listar_pessoas')
    json_pessoas = dados_pessoas.json()
    pessoas = []
    for pessoa_em_json in json_pessoas['lista']:
        p = dict_to_model(Pessoa, pessoa_em_json)
        pessoas.append(p)
    
    return render_template("listar_pessoas.html", lista = pessoas)

@app.route("/listar_salas")
def listar_salas():
    dados_salas = requests.get('http://localhost:5000/listar_salas_primeiro_periodo')
    print(dados_salas)
    json_salas = dados_salas.json()
    salas = []
    for sala_em_json in json_salas['lista']:
        p = dict_to_model(Sala, sala_em_json)
        salas.append(p)

    dados_salas_seg_periodo = requests.get('http://localhost:5000/listar_salas_segundo_periodo')
    print(dados_salas_seg_periodo)
    json_salas = dados_salas_seg_periodo.json()
    salas_seg_periodo = []
    for sala_em_json in json_salas['lista']:
        p = dict_to_model(Sala, sala_em_json)
        salas_seg_periodo.append(p)

    dados_pessoas = requests.get('http://localhost:5000/listar_pessoas')
    json_pessoas = dados_pessoas.json()
    lista_de_pessoas = json_pessoas['lista']
    pessoas = []
    for pessoa_em_json in lista_de_pessoas:
        p = dict_to_model(Pessoa, pessoa_em_json)
        pessoas.append(p)

    dados_cafeterias = requests.get('http://localhost:5000/listar_cafeterias')
    json_cafeterias = dados_cafeterias.json()
    cafeterias = []
    for cafeterias_em_json in json_cafeterias['lista']:
        p = dict_to_model(SalaDeCafe, cafeterias_em_json)
        cafeterias.append(p)
    
    return render_template("listar_salas.html", salas = salas, pessoas = pessoas, cafeterias = cafeterias, salas_seg_periodo= salas_seg_periodo)

@app.route("/form_incluir_pessoa")
def abre_formulario_incluir_pessoa():
    return render_template('form_incluir_pessoa.html')

@app.route("/ajuda")
def ajuda():
    return render_template('ajuda.html')

@app.route("/cadastrar_pessoa", methods=['post'])
def cadastrar_pessoa():
    nome = request.form["nome"]
    sobrenome = request.form["sobrenome"] 
    par = {"nome":nome, "sobrenome":sobrenome}
    req = requests.post(url='http://localhost:5000/cadastrar_pessoa', json=par)
    return render_template('index.html')

@app.route("/form_incluir_sala")
def abre_formulario_incluir_sala():
    return render_template('form_incluir_sala.html')

@app.route("/cadastrar_sala", methods=['post'])
def cadastrar_sala():
    nome = request.form["nome"]
    lotacao_maxima = request.form["lotacao_maxima"] 
    par = {"nome":nome, "lotacao_maxima":lotacao_maxima}
    req = requests.post(url='http://localhost:5000/cadastrar_sala', json=par)
    return render_template('index.html')

@app.route("/form_incluir_cafeteria")
def abre_formulario_incluir_cafeteria():
    return render_template('form_incluir_cafeteria.html')

@app.route("/cadastrar_cafeteria", methods=['post'])
def cadastrar_faceteria():
    nome = request.form["nome"]
    par = {"nome":nome}
    req = requests.post(url='http://localhost:5000/cadastrar_cafeteria', json=par)
    return render_template('index.html')


app.run(debug=True, port=4999)