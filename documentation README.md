# Expected endpoints and behaviors

## GET '/categories'
1. Fetches a dictionary of categories in which the keys are the ids and the values are the corresponding category names
2. Request Arguments: None
3. Returns: An object with keys and categories.
 ```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
```

## GET '/questions?page=${integer}'

    Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    Request Arguments: page - integer
    Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}

GET '/categories/${id}/questions'

    Fetches questions for a cateogry specified by id request argument
    Request Arguments: id - integer
    Returns: An object with questions for the specified category, total questions, and current category string

{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}

DELETE '/questions/${id}'

    Deletes a specified question using the id of the question
    Request Arguments: id - integer
    Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

POST '/quizzes'

    Sends a post request in order to get the next question
    Request Body:

{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }

    Returns: a single new question object

{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}

POST '/questions'

    Sends a post request in order to add a new question
    Request Body:

{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}

    Returns: Does not return any new data

POST '/questions'

    Sends a post request in order to search for a specific question by search term
    Request Body:

{
    'searchTerm': 'this is the term the user is looking for'
}

    Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}


