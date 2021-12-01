import datetime
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import EditNoteForm, ConfirmDeleteNoteForm
from app.models import Note


@app.route("/")
def index():
    title = "Dream Journal"
    notes = Note.query.order_by(Note.date_modified.desc()).all()
    return render_template("index.html", title=title, notes=notes)


@app.route("/new", methods=["GET", "POST"])
def new_note():
    """Create a new note"""
    title = "New Note"
    form = EditNoteForm()
    # validate_on_submit() only tries to validate on POST, so we don't
    # have to check which method was used for the request.
    if form.validate_on_submit():
        # Note we *should* be using datetime.utcnow(). It's always best
        # to store dates and times in UTC in the database, and convert
        # to the local timezone in the app or template.
        new_note = Note(
            date_modified = datetime.datetime.now(),
            title = form.note_title.data,
            body = form.note_body.data
        )
        db.session.add(new_note)
        db.session.commit()
        flash(f"New note created: {new_note.title}")
        return redirect(url_for('index'))

    return render_template("edit.html", title=title, form=form)


@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    """Edit an existing note"""
    title = "Edit Note"
    # Check if the note exists, not just whether the id is between 1 and
    # the highest note id. When notes are deleted, it's possible for the
    # id's to be non-contiguous (e.g. 1 2 3 5 6 8...)
    if db.session.query(Note.id).filter_by(id=note_id).one_or_none() is None:
        flash("No note found with this ID")
        return redirect(url_for('index'))
    # Now that we know it exists, retrieve the note to edit
    note_to_edit = Note.query.filter_by(id=note_id).one_or_none()

    form = EditNoteForm()
    if form.validate_on_submit():
        # The Note object returned from the query is mutable, and
        # automatically part of the current db.session. This means we
        # can edit the variable in place and just commit the changes. No
        # need to create a new variable, or run the equivalent of an
        # "UPDATE" SQL query.
        note_to_edit.date_modified = datetime.datetime.now()
        note_to_edit.title = form.note_title.data
        note_to_edit.body = form.note_body.data
        db.session.commit()
        flash(f"Note updated: {note_to_edit.title}")
        return redirect(url_for('index'))

    # The form wasn't submitted at this point, so we're going to render
    # the form with the existing note's content.
    # We are preloading the form elements with the note content here,
    # before sending everything over to the template. Normally we would
    # send the note_data over to the template, and use it when rendering
    # the form inputs over there. Unfortunately, WTForms can't
    # currently do that with a `<textarea>`. So instead of e.g.:
    # {{ form.note_title(autofocus="", maxlength="80", value=note_data["title"]) }}
    # ...we're just adding the note data to the form object before it
    # gets sent over. Luckily this works for both kinds of form inputs.
    form.note_title.data = note_to_edit.title
    form.note_body.data = note_to_edit.body

    return render_template("edit.html", title=title, form=form)


@app.route("/delete/<int:note_id>", methods=["GET", "POST"])
def delete_note(note_id):
    """Confirm deleting a note"""
    title = "Delete Note"
    # Check if the note exists, redirect to index if not
    if db.session.query(Note.id).filter_by(id=note_id).one_or_none() is None:
        flash("No note found with this ID")
        return redirect(url_for('index'))
    # Now that we know it exists, retrieve the note to delete
    note_to_delete = Note.query.filter_by(id=note_id).one_or_none()

    form = ConfirmDeleteNoteForm()
    if form.validate_on_submit():
        db.session.delete(note_to_delete)
        db.session.commit()
        flash(f"Note deleted")
        return redirect(url_for('index'))

    return render_template("confirm-delete.html",
                           title=title,
                           note_title=note_to_delete.title,
                           form=form)