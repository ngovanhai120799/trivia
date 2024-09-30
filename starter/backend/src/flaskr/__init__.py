import logging
from typing import List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from starter.backend.src.models import Category, Question, db

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1.0/*": {"origins": "*"}})
QUESTIONS_PER_PAGE = 10

'''ToDo Tasks'''


# 1. Use Flask-CORS to enable cross-domain requests and set response headers.
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


# 2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions)
@app.route('/api/v1.0/questions', methods=['GET'])
@cross_origin()
def get_questions():
    page = request.args.get('pages', 1, int)
    row_to_skip = (page - 1) * QUESTIONS_PER_PAGE
    # Get all questions
    query_result = Question.query.limit(QUESTIONS_PER_PAGE).offset(row_to_skip)

    page_result = page_result_json(list(query_result))
    return page_result


# 3. Create an endpoint to handle GET requests for all available categories.
@app.route('/api/v1.0/categories', methods=['GET'])
@cross_origin()
def get_categories():
    categories = get_all_categories()
    return jsonify(categories)


# 4. Create an endpoint to DELETE question using a question ID.
@app.route('/api/v1.0/questions', methods=['POST'])
@cross_origin()
def create_questions():
    try:
        request_body = request.get_json()
        question = request_body.get('question')
        answer = request_body.get('answer')
        category = request_body.get('category')
        difficulty = request_body.get('difficulty')

        question = Question(question, answer, category, difficulty)
        question.insert()
        return jsonify({'status_code': 200})
    except SQLAlchemyError as err:
        logging.info(f'Create question fail: {err}')
        db.session.rollback()


# 5.Create an endpoint to DELETE question using a question ID.
@app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
@cross_origin()
def delete_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        question.delete()
        return jsonify({'status_code': 200})
    except SQLAlchemyError as err:
        logging.info(f'Delete question fail: {err}')
        db.session.rollback()


# 6. Create a POST endpoint to get questions based on category.
@app.route('/api/v1.0/categories/<int:category_id>/questions', methods=['POST'])
@cross_origin()
def get_question_by_category_id(category_id):
    category = Category.query.get_or_404(category_id)
    page_result = page_result_json(category.questions, category.format(), None)
    return page_result


# 7. Create a POST endpoint to get questions based on a search term.
@app.route('/api/v1.0/questions/search', methods=['POST'])
@cross_origin()
def search_question():
    search_term = request.get_json().get('searchTerm')
    query_result = Question.query.filter(Question.question.contains(search_term))

    page_result = page_result_json(list(query_result))
    return page_result


# 8. Create a POST endpoint to get questions to play the quiz
@app.route('/api/v1.0/quizzes', methods=['POST'])
@cross_origin()
def play_quiz():
    request_body = request.get_json()
    previous_questions: List[dict] = request_body.get('previous_questions', [])
    quiz_category: dict = request_body.get('quiz_category', {})

    previous_question_ids = [q['id'] for q in previous_questions]

    # Get random question within the given category if provided
    question = Question.query.filter(Question.id.notin_(previous_question_ids))
    if quiz_category:
        question = question.filter(Question.category == quiz_category['id'])
    question = question.order_by(func.random()).first()
    return jsonify(question.format()) if question else {}


def get_all_categories():
    query_result = Category.query.all()
    categories = {}
    for category in query_result:
        categories[category.id] = category.type
    return categories


def page_result_json(questions: List[Question], current_category: Optional[dict] = None,
                     categories: Optional[dict] = None):
    return jsonify({
        'questions': [q.format() for q in questions] if questions else [],
        'total_questions': len(questions),
        'categories': categories,
        'current_category': current_category
    })
