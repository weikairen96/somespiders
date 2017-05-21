#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,request, make_response
from  flask_script import Manager,Shell
from  flask_migrate import Migrate,MigrateCommand
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
manager=Manager(app)
bootstrap = Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    website=db.Column(db.String(10),index=True)
    title = db.Column(db.Text)
    date = db.Column(db.String(12))
    url = db.Column(db.Text,index=True)
    text = db.Column(db.Text)
    attachments = db.relationship('Attachments', backref='news', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.title
class Attachments(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.Text)
    url=db.Column(db.Text)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __repr__(self):
        return '<Role %r>' % self.name
class Videos(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    video_description=db.Column(db.Text)
    video_img = db.Column(db.Text)
    video_url = db.Column(db.Text,index=True)
    vedio_digg_count = db.Column(db.Integer)

    def __repr__(self):
        return '<Role %r>' % self.video_description



def make_shell_context():


    return dict(app=app, db=db, News=News,Attachments=Attachments,Videos=Videos)
manager.add_command("shell", Shell(make_context=make_shell_context))

















@app.route('/')
def index():
    news = News.query.order_by(News.date.desc()).all()
    return render_template('index.html',news=news)

@app.route('/new/<int:id>/')
def detail_new(id):
    new=News.query.filter_by(id=id).first()
    if(new):
        return render_template('detail_new.html',new=new)
    else:
        return render_template('404.html')
@app.route('/videos/')
def videos():
    videos = Videos.query.limit(5)
    return render_template('videos.html',videos=videos)


@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
