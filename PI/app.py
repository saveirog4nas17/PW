from flask import Flask, render_template, request, redirect, session, url_for,flash
from werkzeug.utils import secure_filename
from playhouse.shortcuts import  model_to_dict
import os
from tabelas import Pessoa, Produto, Pedidos, Empresa, PedidoProduto


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", empresas = Empresa.select())

@app.route ("/login/")
def logar():
    if session.has_key("usuario"):
        return redirect("/")
    return render_template("login.html")

@app.route("/cadastro/", methods=['GET', 'POST'])
def cadastro():
    if session.has_key("usuario"):
        return redirect("/")
    return render_template("cadastro.html")

@app.route ("/cadastroempresa/")
def cadastroempresa():
	if not session.has_key("usuario"):
	    return redirect("/login/")
	return render_template("cadastroempresa.html",usuarioLogado=session['usuario'])

@app.route ("/alterar/")
def alterar():
	if not session.has_key("usuario"):
	    return redirect("/login/")
	return render_template("alterar.html",usuarioLogado=session['usuario'])

@app.route ("/sobre/")
def sobre():
	if not session.has_key("usuario"):
	    return redirect("/login/")
	return render_template("sobre.html",usuarioLogado=session['usuario'])

@app.route ("/inserir/")
def inserir():
	empresas = Empresa.lista()
	if not session.has_key("usuario"):
		return redirect("/login/")
	return render_template("inserir.html",usuarioLogado=session['usuario'], empresas = empresas)

@app.route ("/detalhes/<id>/")
def detalhes(id):
	if not session.has_key("usuario"):
		return redirect("/login/")
	pedido, criado = Pedidos.get_or_create(pessoa = session['id'], estadoPedido="comprando")
	empresa = Empresa.get_by_id(int(id))
	produtos = empresa.produtos
	if not session.has_key("usuario"):
		return redirect("/login/")
	itens = Produto.select()
	return render_template("detalhes.html",usuarioLogado=session['usuario'], **locals())

@app.route ("/pedidos/")
def pedidos():
	pedidos = Pedidos.select()
	if not session.has_key("usuario"):

		return redirect("/login/")
	return render_template("pedidos.html",usuarioLogado=session['usuario'], **locals())

@app.route ("/perfil/")
def perfil():
    if not session.has_key("usuario"):
        return redirect("/login/")
	#print("!>>>>>>Id=" + session["id"])
	#pessoa = Pessoa.get_by_id(session["id"])
    return render_template("perfil.html", usuarioLogado=session['usuario'], session=session)

@app.route ("/recuperarsenha/")
def recuperarsenha():
	return render_template("recuperarsenha.html")

@app.route ("/senhaAlterada/<id>/")
def senhaAlterada(id):
	p = Pessoa.get_by_id(id)
	return render_template("senhaalterada.html", p=p)

@app.route("/novasenha/", methods=["GET","POST"])
def novasenha():
	if request.method=="POST":
		try:
			if request.form['email'] == "":
				raise Exception(u"Informe o email")
			if request.form['frase'] == "":
				raise Exception(u"Informe a frase secreta")
			emailAlterar = request.form['email']
			frase = request.form['frase']
			try:

				p = Pessoa.select().where(Pessoa.email == emailAlterar and Pessoa.frase == frase).get()
			except:
				raise Exception(u"Este email nao existe")
			

			p.senha = "mudarsenha"
			p.save()
			return redirect("/senhaAlterada/%d/" %p.id)
		except Exception as error:
			return render_template("recuperarsenha.html", msg_error = error,	form={})
	else:
		return render_template("recuperarsenha.html", form={})

def processa_upload(name_do_input):
	if name_do_input not in request.files:
		return ""
	else:
		arquivo_temporario = request.files[name_do_input]
		nome_do_arquivo = secure_filename(arquivo_temporario.filename)
		caminho_do_arquivo = "static/uploads/" + nome_do_arquivo
		arquivo_temporario.save(caminho_do_arquivo)
		url_do_arquivo = "/"+caminho_do_arquivo
		return url_do_arquivo

@app.route("/cadastrar/", methods=["GET","POST"])
def cadastrar():
	if request.method=="POST":
		try:
			if request.form['usuario'] == "":
				raise Exception(u"Informe o usuario")	
			if request.form['senha'] == "":
				raise Exception(u"informe a senha")
			if (request.form['senha'] != request.form['confirma_senha']):
				raise Exception(u"Senhas diferentes")
			p = Pessoa()
			p.usuario = request.form['usuario'] 
			p.email = request.form['email']
			p.senha = request.form['senha']
			p.frase = request.form['frase']

			p.cidade = request.form['cidade']
			p.bairro = request.form['bairro']
			p.rua = request.form['rua']
			p.numero = request.form['numero']
			p.foto_url = processa_upload("foto_url")
			p.save()
			return redirect("/")
		except Exception as error:
			return render_template("cadastro.html", msg_error = error,	form={})
	else:
		return render_template("cadastro.html", form={})

@app.route("/cadastrarempresa/", methods=["GET","POST"])
def cadastrarempresa():
	if request.method=="POST":
		try:
			if request.form['nome'] == "":
				raise Exception(u"Informe o nome da empresa")	
			p = Empresa()
			p.nome = request.form['nome'] 
			p.save()
			return redirect("/")
		except Exception as error:
			return render_template("cadastroempresa.html", msg_error = error,	form={})
	else:
		return render_template("cadastroempresa.html", form={})

@app.route("/adicionar/", methods=["GET","POST"])
def adicionar():
	
	form={}
	
	if request.method=="POST":
		try:
			if request.form['item'] == "":
				raise Exception(u"Informe o item a ser cadastrado")	
			p = Produto()
			p.empresa = int(request.form.get("empresa"))
			p.nome = request.form['item']
			p.valor = request.form['valor']
			p.categoria = request.form['categoria']
			p.save()
			return redirect("/inserir/")
		except Exception as error:
			msg_error = error
			return render_template("inserir.html", **locals())
	else:
		return render_template("index.html", **locals())

@app.route("/adicionarProdutoAoPedido/<produto_id>/<empresa_id>/", methods=["GET","POST"])
def meuspedidos(produto_id, empresa_id):
	pedido, criado = Pedidos.get_or_create(pessoa = session['id'], estadoPedido="comprando")
	pedido.save()

	propedido = PedidoProduto()
	propedido.pedido = pedido.id
	propedido.produto = produto_id
	propedido.save()
	return redirect("/detalhes/%s/" % empresa_id)

@app.route("/finalizar/")
def finalizar():
	
	pedido = Pedidos.get(pessoa=int(session["id"]), estadoPedido="comprando")
	pedido.estadoPedido = "Finalizado"
	pedido.save()
	return redirect("/")

@app.route("/terminar/<id>/")
def terminar(id):
	Pedidos.delete().where(Pedidos.id == id).execute()


	return redirect("/pedidos/")
	


@app.route("/logar/",methods =["POST"]) 
def login (): 
    usuario = request.form["usuario"] 
    senha = request.form["senha"] 
    try:
		pessoa = Pessoa.select().where(Pessoa.usuario == usuario and Pessoa.senha == senha).get()
		session["usuario"]=usuario
		session["id"]= pessoa.id
		session["foto_url"]=pessoa.foto_url
		session["email"]=pessoa.email
		session["cidade"]=pessoa.cidade
		return redirect("/")
        
    except Exception as error:
        flash('Usuario ou senha incorretos')
        flash('Digite novamente por favor')
        return redirect("/login/")

app.secret_key = 'auishdiuahsydhgasyd'

@app.route("/logout/")
def logout():
    session.pop("usuario", None)
    return redirect("/login/")


@app.route("/alterar/<id>/", methods=["GET","POST"])
def atualizar(id):
    
	if request.method=="POST":
		try:
			if request.form['usuario'] == "":
				raise Exception(u"usuario nao informado")	
			if request.form['email'] == "":
				raise Exception(u"email nao informado")
			if request.form['senha'] == "":
				raise Exception(u"senha nao informada")

			p = Pessoa.get_by_id(id)
			p.usuario = request.form['usuario'] 
			p.email = request.form['email']
			p.senha = request.form['senha']
			p.frase = request.form['frase']
			p.cidade = request.form['cidade']
			p.bairro = request.form['bairro']
			p.rua = request.form['rua']
			p.numero = request.form['numero']
			p.foto_url = processa_upload("foto_url")
			p.save()
			return redirect("/perfil/")
		except Exception as error:
			return render_template("alterar.html", id = id,  msg_error = error, form = request.form.to_dict())
	else:
		p = Pessoa.get(id)
		return render_template("alterar.html", id = id, form=model_to_dict(p))

@app.route("/remover/<id>/", methods=['GET', 'POST'])
def remover(id):
	pessoa = Pessoa.get_by_id(id)
	caminho_foto = pessoa.foto_url[1:]
	os.unlink(caminho_foto)
	Pessoa.delete().where(Pessoa.id==id).execute()
	finalizar()
	return redirect("/logout/")





