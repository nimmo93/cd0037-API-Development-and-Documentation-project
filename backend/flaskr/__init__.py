import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


'''
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

'''
    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app)
    #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.

    """
    
    @app.route('/categories')
    def retrieve_categories():
        total_categories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in total_categories]
        
        if len(total_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })
    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)


        

        total_categories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in total_categories]
        
        #category = Question.query.filter_by(category=Question.category).all()
       

        if len(current_questions) == 0:
           abort(404)
        
        return jsonify(
            {
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories' : categories,
                'current_category': None
                
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len( Question.query.all())
            })
        except:
            abort(422)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        
 
        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            
            question.insert()

           
            return jsonify({
                'success': True,
                'created': question.id,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)
    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_by_category(category_id):

        try:
            questions = Question.query.filter(Question.category == category_id).all()

            selected_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': selected_questions,
                'current_category': category_id,
                'total_questions': len(selected_questions)
            })
        except:
            abort(404)

     
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        try: 
            selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(current_questions)

            })
        except:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

 
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()


        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')


        try:
            selection = Question.query.filter(Question.category == quiz_category).all()
            current_questions = [question.format() for question in selection]

            if current_questions != previous_questions:
                for i in current_questions:
                    i = current_questions[random.randrange(0, len(current_questions))]
             
            
            return jsonify({
                'success': True,
                'question': [i]
            })
        except:
            abort(422)
       
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message':'resource not found'
        }), 404    
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'this is a bad request'
        }), 400
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    

   

   

   


   

    
   
   
   
   
    return app

