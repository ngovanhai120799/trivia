###### 1. Create an endpoint to handle GET requests for all available categories.
`GET '/api/v1.0/categories'`
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None
* Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
```
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  }
```

###### 2. Create an endpoint to handle GET requests for questions
`GET '/api/v1.0/questions'`
* Fetches list of questions, including pagination (every 10 questions)
* Request Arguments: None
* Returns: An object with a list of questions, number of total questions, current category, categories.
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "total_questions": 1
}
```

###### 3. Create an endpoint to DELETE question using a question ID.

`DELETE '/api/v1.0/questions/<int:id>'`
* DELETE question using a question ID
* Request Arguments: None
* Returns: An object with a list of questions, number of total questions, current category, categories.
```
{
    "status_code": 200
}
```

###### 4. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
`POST '/api/v1.0/questions/'`
* DELETE question using a question ID
* Request Arguments:
```
{
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "question": "What is the largest lake in Africa?"
}
```
* Returns: An object with a list of questions, number of total questions, current category, categories.
```
{
    "status_code": 200
}
```

###### 5. Create a POST endpoint to get questions based on category.
`POST '/api/v1.0/categories/<int:category_id>/questions'`
* Fetches list of questions, including pagination (every 10 questions)
* Request Arguments: None
* Returns: An object with a list of questions, number of total questions, current category, categories.
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "total_questions": 1
}
```

###### 6. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
   `POST '/api/v1.0/questions'`
* Create a POST endpoint to get questions based on a search term
* Request Arguments:
```
{
    "searchTerm": "Which dung beetle was worshipped by the ancient Egyptians?"
}
```
* Returns: An object with a list of questions, number of total questions, current category, categories.
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "total_questions": 1
}
```

###### 7. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

`POST '/api/v1.0/quizzes'`
* This endpoint should take category and previous question parameters
* Request Arguments:
```
{
    "previous_questions": [],
    "quiz_category" : {
        "id": 1,
        "type": "History"
    }
}
```
* Returns: A random questions within the given category, if provided, and that is not one of the previous questions.
```
{
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
}
```
