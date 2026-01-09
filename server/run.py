#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/jerry/snap/code/217/.local/share/virtualenvs/python-p4-flask-restful-ud-MqR6MC3a/lib/python3.8/site-packages')

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Flask-RESTful Newsletter API")
    print("=" * 60)
    print("\nServer running at: http://127.0.0.1:5555")
    print("\nAvailable endpoints:")
    print("  GET    /                    - Welcome message")
    print("  GET    /newsletters         - Get all newsletters")
    print("  POST   /newsletters         - Create new newsletter")
    print("  GET    /newsletters/<id>    - Get newsletter by ID")
    print("  PATCH  /newsletters/<id>    - Update newsletter")
    print("  DELETE /newsletters/<id>    - Delete newsletter")
    print("\nPress CTRL+C to stop\n")
    print("=" * 60)
    app.run(port=5555, debug=True)
