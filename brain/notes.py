"""
=========================================================
Project G-EXO
Notes Storage Module
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

import json
import os


NOTES_FILE = "brain/notes.json"


def load_notes():

    if not os.path.exists(NOTES_FILE):

        with open(NOTES_FILE, "w") as file:

            json.dump([], file, indent=4)

    with open(NOTES_FILE, "r") as file:

        return json.load(file)


def save_notes(notes):

    with open(NOTES_FILE, "w") as file:

        json.dump(notes, file, indent=4)


def add_note(text):

    notes = load_notes()

    notes.append(text)

    save_notes(notes)


def get_notes():

    return load_notes()


def delete_note(index):

    notes = load_notes()

    if 0 <= index < len(notes):

        notes.pop(index)

        save_notes(notes)

        return True

    return False


def clear_notes():

    save_notes([])