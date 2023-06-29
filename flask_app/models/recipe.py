from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask import flash
from flask_app.models.user import User

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL(DB).query_db(query)
        
        recipes = []
        for row in results:
            # Creating an instance of the review
            recipe = cls(row)

            # Dictionary to create the User instance
            user_dict = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }

            recipe.user = User(user_dict)
            recipes.append(recipe)

        return recipes
    
    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        
        results = connectToMySQL(DB).query_db(query, data)

        if len(results) < 1:
            return False
        
        row = results[0]

        recipe = cls(row)
        
        user_dict = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at'],
        }

        recipe.user = User(user_dict)
        return recipe

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(date_made)s, %(user_id)s);"
        results = connectToMySQL(DB).query_db(query , data)
        return results
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, date_made = %(date_made)s, user_id = %(user_id)s WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return results
    
    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validation(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("name must be at least 3 characters!","recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("description must be at least 3 characters!","recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("instructions must be at least 3 characters!","recipe")
            is_valid = False
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid


