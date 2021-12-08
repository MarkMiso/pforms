from pforms import create_app
from pforms.extensions import db
from pforms.models import User, Category

app = create_app()
with app.app_context():
    db.create_all()

    sport = Category(name='sport')
    deleted = User(username='deleted', email='deleted', password='dbfaodfnalnfpsdfiwelsdfoisl')

    db.session.add(sport)
    db.session.add(deleted)

    db.session.commit()