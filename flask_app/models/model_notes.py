from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import bcrypt, DATABASE

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Note:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under_30_minutes = data['under_30_minutes']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM notes;"
        results = connectToMySQL(DATABASE).query_db(query)
        
        if results:
            notes_list =[]
            for person in results:
                notes_list.append(cls(person))
            return notes_list
        return []

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM notes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    @staticmethod
    def validator(form_data):
        is_valid = True

        if len(form_data['name']) < 2:
            is_valid = False
            flash('Must enter Name', 'err_notes_name')
        
        if len(form_data['description']) < 2:
            is_valid = False
            flash('Must enter Description', 'err_notes_description')

        if len(form_data['instructions']) < 2:
            is_valid = False
            flash('Must enter Instructions', 'err_notes_instructions')



        return is_valid
