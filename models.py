from bibliotech import db


class Tecnologias(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        nome = db.Column(db.String(30), nullable=False)
        descricao = db.Column(db.String(250), nullable=False)
        nivel = db.Column(db.String(30), nullable=False)
        criador = db.Column(db.String(60), nullable=False)
        ano_lancamento = db.Column(db.Integer, nullable=False)
        categorias = db.Column(db.String(255), nullable=False)
        recursos = db.Column(db.String(200), nullable=False)

        def __repr__(self):
            return '<Name %r>' % self.nome

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome