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
video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)


# db.create_all() --This should be run only once at the start of the app, commented out because if ran each time, db will reinitialize each time.

# Create A video
@app.route('/video', methods=['POST'])
def add_video():
    name = request.json['name']
    views = request.json['views']
    likes = request.json['likes']

    new_video = VideoModel(name, views, likes)

    db.session.add(new_video)
    db.session.commit()

    return video_schema.jsonify(new_video)


# Update A video
@app.route('/video/<id>', methods=['PUT'])
def update_video(id):
    video = VideoModel.query.get(id)

    name = request.json['name']
    views = request.json['views']
    likes = request.json['likes']

    video.name = name
    video.views = views
    video.likes = likes

    db.session.commit()

    return video_schema.jsonify(video)


# get all videos list
@app.route('/video', methods=['GET'])
def get_videos():
    all_videos = VideoModel.query.all()
    result = videos_schema.dump(all_videos)
    return jsonify(result)


# get one video
@app.route('/video/<id>', methods=['GET'])
def get_video(id):
    video = VideoModel.query.get(id)
    return video_schema.jsonify(video)


# delete video
@app.route('/video/<id>', methods=['DELETE'])
def delete_video(id):
    video = VideoModel.query.get(id)
    db.session.delete(video)
    db.session.commit()
    return video_schema.jsonify(video)


# run Server
if __name__ == '__main__':
    app.run(debug=True)
