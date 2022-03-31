from turtle import title
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db" #Linha para o arquivo do banco de dados
#Iniciando o banco de dados
db = SQLAlchemy(app)

#Criar um model do database
class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False) #200 é o maximo de caracteres
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    #Função para retornar uma string quando adicionar algo ao banco
    def __repr__(self):
        return '<Name %r>' % self.id


@app.route("/")
def index():
    return render_template("index.html", active="index", title="Home", page_title="Home") 

@app.route("/produtos/")
def listarProdutos():
    produtos = Estoque.query.order_by(Estoque.data_cadastro)
    return render_template('produtos.html', lista_produtos=produtos, active="produtos", title="Produtos", page_title="Produtos")

@app.route("/produtos/adicionar", methods=['POST', 'GET'])
def adicionarProdutos():

    if request.method == "POST":
        produto_name = request.form['nome']
        new_produto = Estoque(produto=produto_name)
        
        #Mandar para o database
        try:
            db.session.add(new_produto)
            db.session.commit()
            return redirect("/produtos")
        except:
            return "Ocorreu um erro ao adicionar o produto!"
    else:
        produtos = Estoque.query.order_by(Estoque.data_cadastro)
        return render_template('form.html', produtos=produtos)