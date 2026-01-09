#!/usr/bin/env python3
import sys
import os
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

# Models
class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'published_at': str(self.published_at) if self.published_at else None,
            'edited_at': str(self.edited_at) if self.edited_at else None
        }

# Initialize API
api = Api(app)

# Resources
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        response = make_response(response_dict, 200)
        return response

class Newsletters(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        response = make_response(response_dict_list, 200)
        return response
    
    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(response_dict, 201)
        return response

class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if not newsletter:
            return make_response({"error": "Newsletter not found"}, 404)
        response_dict = newsletter.to_dict()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": "Newsletter not found"}, 404)
        
        for attr in request.form:
            setattr(record, attr, request.form[attr])
        
        db.session.add(record)
        db.session.commit()
        response_dict = record.to_dict()
        response = make_response(response_dict, 200)
        return response
    
    def delete(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": "Newsletter not found"}, 404)
        
        db.session.delete(record)
        db.session.commit()
        response_dict = {"message": "record successfully deleted"}
        response = make_response(response_dict, 200)
        return response

# Register resources
api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    print("=" * 60)
    print("Flask-RESTful Newsletter API - PATCH & DELETE Tutorial")
    print("=" * 60)
    print("\nServer: http://127.0.0.1:5555")
    print("\nEndpoints:")
    print("  GET    /                    - Welcome message")
    print("  GET    /newsletters         - Get all newsletters")
    print("  POST   /newsletters         - Create newsletter")
    print("  GET    /newsletters/<id>    - Get newsletter by ID")
    print("  PATCH  /newsletters/<id>    - Update newsletter")
    print("  DELETE /newsletters/<id>    - Delete newsletter")
    print("\nPress CTRL+C to stop\n")
    print("=" * 60)
    app.run(port=5555, debug=True, use_reloader=False)
