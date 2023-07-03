from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from bibliotech import app, db
from models import Tecnologias
from helpers import recupera_imagem, deleta_arquivo, FormularioTecnologia
import time

@app.route('/')
def index():
    lista_tecnologias = Tecnologias.query.order_by(Tecnologias.id)
    return render_template('lista.html', titulo='Lista de tecnologias', tecnologias = lista_tecnologias)

#--------------------------------------CRIAR--------------------------------------


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioTecnologia()
    return render_template('novo.html', titulo='Adicionar Tecnologia', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioTecnologia(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    descricao = form.descricao.data
    nivel = form.nivel.data
    criador = form.criador.data
    ano_lancamento = form.ano_lancamento.data
    categorias = form.categorias.data
    recursos = form.recursos.data

    tecnologia = Tecnologias.query.filter_by(nome=nome).first()

    if tecnologia:
        flash('Tecnologia já existente na tabela!')
        return redirect(url_for('index'))

    tech = Tecnologias(nome=nome,descricao=descricao,nivel=nivel,criador=criador,ano_lancamento=ano_lancamento,categorias=categorias,recursos=recursos)
    db.session.add(tech)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/icon{tech.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

#--------------------------------------EDITAR/ATUALIZAR--------------------------------------


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    tech = Tecnologias.query.filter_by(id=id).first()
    form = FormularioTecnologia()
    form.nome.data = tech.nome
    form.descricao.data = tech.descricao
    form.nivel.data = tech.nivel
    form.criador.data = tech.criador
    form.ano_lancamento.data = tech.ano_lancamento
    form.categorias.data = tech.categorias
    form.recursos.data = tech.recursos
    
    icon_tech = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Tecnologia', id=id, icon_tech=icon_tech, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioTecnologia(request.form)

    if form.validate_on_submit():
        tecnologia = Tecnologias.query.filter_by(id=request.form['id']).first()
        tecnologia.nome = form.nome.data
        tecnologia.descricao = form.descricao.data
        tecnologia.nivel = form.nivel.data
        tecnologia.criador = form.criador.data
        tecnologia.ano_lancamento = form.ano_lancamento.data
        tecnologia.categorias = form.categorias.data
        tecnologia.recursos = form.recursos.data

        db.session.add(tecnologia)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/icon{tecnologia.id}-{timestamp}.jpg')

    return redirect(url_for('index'))







#--------------------------------------DELETAR--------------------------------------

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Tecnologias.query.filter_by(id=id).delete()

    db.session.commit()
    flash('Tecnologia deletada com sucesso.')

    return redirect(url_for('index'))




@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
    


