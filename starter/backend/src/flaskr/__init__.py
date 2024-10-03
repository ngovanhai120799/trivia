from typing import List, Optional

from flask import Flask, request, jsonify, abort, Blueprint
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from starter.backend.src.models import Category, Question, db
QUESTIONS_PER_PAGE = 10

'''ToDo Tasks'''
api = Blueprint('api', __name__, url_prefix='/api/v1.0/')


# 1. Use Flask-CORS to enable cross-domain requests and set response headers.
@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

# 2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions)
@api.route('/questions', methods=['GET'])
@cross_origin()
def get_questions():
    try:
        page = request.args.get('page', 1, int)
        row_to_skip = (page - 1) * QUESTIONS_PER_PAGE
        # Get all questions
        query_result = Question.query
        questions = query_result.limit(QUESTIONS_PER_PAGE).offset(row_to_skip)
        categories = get_all_categories()

        page_result = page_result_json(list(questions), categories=categories, total_questions=query_result.count())
        return page_result
    except SQLAlchemyError as err:
        abort(400, f'Get ALL questions fail: {err}')


# 3. Create an endpoint to handle GET requests for all available categories.
@api.route('/categories', methods=['GET'])
@cross_origin()
def get_categories():
    try:
        categories = get_all_categories()
        page_result = page_result_json(questions=[], categories=categories)
        return page_result
    except SQLAlchemyError as err:
        abort(400, f'Get ALL questions fail: {err}')


# 4. Create an endpoint to DELETE question using a question ID.
@api.route('/questions', methods=['POST'])
@cross_origin()
def create_questions():
    try:
        request_body = request.get_json()
        # if search_term is not None, get question contains search_term, else create new question base on body request
        search_term = request_body.get('searchTerm')
        if search_term:
            return search_question(search_term)

        question = request_body.get('question')
        answer = request_body.get('answer')
        category = request_body.get('category')
        difficulty = request_body.get('difficulty')

        question = Question(question, answer, category, difficulty)
        question.insert()
        return jsonify({'status_code': 200})
    except SQLAlchemyError as err:
        db.session.rollback()
        abort(400, f'Create question fail: {err}')


# 5.Create an endpoint to DELETE question using a question ID.
@api.route('/questions/<int:question_id>', methods=['DELETE'])
@cross_origin()
def delete_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        question.delete()
        return jsonify({'status_code': 200})
    except SQLAlchemyError as err:
        db.session.rollback()
        abort(400, f'Delete question fail: {err}')


# 6. Create a POST endpoint to get questions based on category.
@api.route('/categories/<int:category_id>/questions', methods=['POST'])
@cross_origin()
def get_question_by_category_id(category_id):
    category = Category.query.get_or_404(category_id)
    questions = category.questions
    current_category: str = category.type
    categories: dict = get_all_categories()
    total_questions: int = len(questions)
    page_result = page_result_json(questions, current_category, categories, total_questions)
    return page_result


# 8. Create a POST endpoint to get questions to play the quiz
@api.route('/quizzes', methods=['POST'])
@cross_origin()
def play_quiz():
    request_body = request.get_json()
    previous_questions: List[int] = request_body.get('previous_questions', [])
    quiz_category: dict = request_body.get('quiz_category', {})

    # Get random question within the given category if provided
    question = Question.query.filter(Question.id.notin_(previous_questions))
    if quiz_category:
        question = question.filter(Question.category == quiz_category['id'])
    question = question.order_by(func.random()).first()
    return jsonify({"question": question.format()}) if question else {}


def get_all_categories() -> dict:
    query_result = Category.query.all()
    categories: dict = {}
    for category in query_result:
        categories[category.id] = category.type
    return categories


# 9. Create error handlers for all expected errors including 400, 404, 422 and 500.
@api.errorhandler(400)
def resource_bad_request(e):
    return get_response_json_error(400, f'Bad Request: {str(e)}')


@api.errorhandler(404)
def resource_not_found(e):
    return get_response_json_error(404, f'Resource not found: {str(e)}')


@api.errorhandler(422)
def resource_unprocessable(e):
    return get_response_json_error(422, f'Unprocessable Exception: {str(e)}')


@api.errorhandler(500)
def resource_internal_server_error(e):
    return get_response_json_error(500, f'Internal Server Error Exception: {str(e)}')


# 7. Create a POST endpoint to get questions based on a search term.
def search_question(search_term: str):
    query_result = Question.query.filter(Question.question.contains(search_term))
    categories: dict = get_all_categories()
    current_category = query_result.first().categories.type
    if not query_result:
        abort(404, f"Resource not found with search_term: {search_term}")
    page_result = page_result_json(query_result, current_category, categories, query_result.count())
    return page_result


def page_result_json(questions: List[Question], current_category: Optional[str] = None,
                     categories: Optional[dict] = None, total_questions: int = 0):
    return jsonify({
        'questions': [q.format() for q in questions] if questions else [],
        'total_questions': total_questions,
        'categories': categories,
        'current_category': current_category
    })


def get_response_json_error(status_code: int, message: str):
    return jsonify({
        'success': False,
        'error': status_code,
        'message': message
    }), status_code
