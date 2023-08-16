#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = []
    for article in Article.query.all():
        article_dict = article.to_dict()
        articles.append(article_dict)
    response = make_response(
        articles,
        200
    )
    return response 


@app.route('/articles/<int:id>')
def show_article(id):
    article = Article.query.filter(Article.id == id).first()
    if article == None: 
        response_body = {
            "message": "pick an article that actually exists, bro. i mean really...."
        } 
        response = make_response(
            response_body,
            404
        )
        return response 
    else:
        session['page_views'] += 1
        if session['page_views'] <= 3:
            article_dict = article.to_dict()
            article_dict["page_views"] = session['page_views']
            response = make_response(
                article_dict,
                200
            )
            return response
        else:
            response_body = {
                'message': 'Maximum pageview limit reached'
                }
        response = make_response(
            response_body,
            401
        )
        return response  

if __name__ == '__main__':
    app.run(port=5555)
