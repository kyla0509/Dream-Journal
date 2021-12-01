from app import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_modified = db.Column(db.DateTime())
    title = db.Column(db.String(80))
    body = db.Column(db.String(4000))

    # Tell Python how to print objects of this class. Useful when
    # debugging.
    def __repr__(self):
        return '<Note {}>'.format(self.title)