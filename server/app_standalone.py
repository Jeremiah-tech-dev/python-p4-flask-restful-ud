#!/usr/bin/env python3
"""
Test script for Flask-RESTful Newsletter API
Tests GET, POST, PATCH, and DELETE operations
"""

import sys
sys.path.insert(0, '/home/jerry/snap/code/217/.local/share/virtualenvs/python-p4-flask-restful-ud-MqR6MC3a/lib/python3.8/site-packages')

from flask import Flask, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app)
api = Api(app)

# Models
class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) else None 
                for c in self.__table__.columns}

# Resources
class Home(Resource):
    def get(self):
        return {"message": "Welcome to the Newsletter RESTful API"}, 200

class Newsletters(Resource):
    def get(self):
        return [n.to_dict() for n in Newsletter.query.all()], 200
    
    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record.to_dict(), 201

class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if not newsletter:
            return {"error": "Newsletter not found"}, 404
        return newsletter.to_dict(), 200
    
    def patch(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": "Newsletter not found"}, 404
        
        for attr in request.form:
            setattr(record, attr, request.form[attr])
        
        db.session.add(record)
        db.session.commit()
        return record.to_dict(), 200
    
    def delete(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": "Newsletter not found"}, 404
        
        db.session.delete(record)
        db.session.commit()
        return {"message": "record successfully deleted"}, 200

# Register resources
api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    print("Starting Flask-RESTful Newsletter API on http://127.0.0.1:5555")
    print("\nAvailable endpoints:")
    print("  GET    /                    - Welcome message")
    print("  GET    /newsletters         - Get all newsletters")
    print("  POST   /newsletters         - Create new newsletter")
    print("  GET    /newsletters/<id>    - Get newsletter by ID")
    print("  PATCH  /newsletters/<id>    - Update newsletter by ID")
    print("  DELETE /newsletters/<id>    - Delete newsletter by ID")
    print("\nPress CTRL+C to stop the server\n")
    app.run(port=5555, debug=True)
