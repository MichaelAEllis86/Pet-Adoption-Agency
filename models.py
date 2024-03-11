from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below

class Pet(db.Model):
    """Pet model. A 7 column table for notes and indentification for pets available for adoption"""

    __tablename__ = "pets"

    def __repr__(self):
        p=self
        return f"<pet id={p.id} name={p.name} species={p.species} image_url={p.image_url} age={p.age} notes={p.notes} available={p.available} "
    
    def format_available(self):
        """formats the true false for the available boolean column to a friendly string """
        if self.available ==True:
            return "is available for adoption!!"
        else:
            return "has been adopted please look for another pet."
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.Text,
                        nullable=False,
                        unique=False)
    species=db.Column(db.Text,
                        nullable=False,
                        unique=False)
    image_url=db.Column(db.Text, 
                        nullable=True,
                        unique=False,
                        default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDAU07vsdwtne-qkoiEmrp_OhtwgMc6IkvMw&usqp=CAU')
    age=db.Column(db.Integer,
                  nullable=True)
    notes=db.Column(db.Text,
                    nullable=True)
    available=db.Column(db.Boolean,
                        nullable=False,
                        default=True)
    
    
    
