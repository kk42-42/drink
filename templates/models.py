from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vocabulary = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    part_of_speech = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'vocabulary': self.vocabulary,
            'translation': self.translation,
            'part_of_speech': self.part_of_speech
        }