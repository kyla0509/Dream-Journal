from datetime import datetime

from app import db
from app.models import Note


if __name__ == '__main__':
    # Create the database
    db.create_all()

    # Populate it with the same notes from our original variable
    initial_notes = [
        Note(
            date_modified=datetime(2021, 10, 1, 15, 2),
            title="ky",
            body=":D",
        ),
        Note(
            date_modified=datetime(2021, 10, 3, 10, 19),
            title="la",
            body=":)",
        ),
        Note(
            date_modified=datetime(2021, 10, 12, 8, 30),
            title="pog",
            body=":)",
        ),
        Note(
            date_modified=datetime(2021, 10, 18, 19, 37),
            title="champ",
            body=":(",
        )
    ]

    # db.session is a transaction in SQL terminology
    # Collect our notes into the current transaction "queue"
    for note in initial_notes:
        db.session.add(note)

    # Commit our changes to the database all at once. Sometimes we need
    # to make multiple changes to a database, like updating multiple
    # tables. Sometimes if the changes are not all saved successfully it
    # could leave the database in a broken state. By using sessions
    # (transactions), we can queue up all of our changes, then commit
    # them all at once. This way the whole transaction either succeeds
    # and the database is fully updated correctly, or it fails and the
    # database is left unaffected.
    db.session.commit()