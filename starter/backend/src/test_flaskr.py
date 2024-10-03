import os
import unittest

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    os.environ["DB_USERNAME"] = 'postgres'
    os.environ["DB_PASSWORD"] = '1234567890'
    os.environ["DB_NAME"] = 'trivia_test'

    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def test_get_questions(self):
        response = self.client.get('/api/v1.0/questions')
        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        data=dict(question="question", answer="answer", category=1, difficulty="1")
        response = self.client.post('/api/v1.0/questions', json=data, headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_search_question(self):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        data=dict(searchTerm='questions')
        response = self.client.post('/api/v1.0/questions', json=data, headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        response = self.client.get('/api/v1.0/categories')
        self.assertEqual(response.status_code, 200)

    def test_delete_question(self):
        response = self.client.delete('/api/v1.0/questions/2')
        self.assertEqual(response.status_code, 200)

    def test_get_question_by_category_id(self):
        response = self.client.get('/api/v1.0/categories/1/questions')
        self.assertEqual(response.status_code, 200)

    def test_play_quizzes(self):
        data = {
            "previous_questions":[],
            "quiz_category": {"id": 1, "type": "Science"}
        }
        response = self.client.post('/api/v1.0/quizzes', json=data)
        self.assertEqual(response.status_code, 200)

    def test_abort_not_found(self):
        response = self.client.get('/api/v1.0/categories/test_id/questions')
        self.assertEqual(response.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()