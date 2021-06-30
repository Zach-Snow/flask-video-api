from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Video class
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __init__(self, name, views, likes):
        self.name = name
        self.views = views
        self.likes = likes


# Video Schema
class VideoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'views', 'likes')


# Init Schema
video_schema = VideoSchema
videos_schema = VideoSchema(many=True)

# db.create_all() --This should be run only once at the start of the app, commented out because if ran each time, db will reinitialize each time.

# run Server
if __name__ == '__main__':
    app.run(debug=True)
