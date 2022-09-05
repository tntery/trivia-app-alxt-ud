import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgresql://{}:{}@{}/{}".format("student", "student", "localhost:5432", self.database_name)
        self.database_path = os.environ['TRIVIA_APP_DB_PATH']
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who is the best?',
            'answer': 'Me',
            'difficulty': 3,
            'category': 6,
        }

        # self.search_body = 

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_405_for_category_deletion_not_allowed(self):
        res = self.client().delete("/categories")

        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertIsNone(data["current_category"])

    def test_404_requesting_outside_valid_page_rage(self):
        res = self.client().get("/questions?page=30000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/15")
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 15).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 15)
    #     self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/books/2000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_405_if_question_deletion_not_allowed(self):
        res = self.client().delete("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_search_questions(self):
        res = self.client().post("/questions/search", json={ 'searchTerm': 'title' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertIsNone(data["current_category"])

    def test_404_no_question_matches_search_term(self):
        res = self.client().post("/questions/search", json={ 'searchTerm': 'zzzzz' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_question_by_category(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_405_for_get_question_by_category_new_question_not_allowed(self):
        res = self.client().delete("/categories/10/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_quiz_question(self):
        res = self.client().post(
            "/quizzes", 
            json={
                'previous_questions': [], 
                'quiz_category':'4',
                }
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_405_for_get_quiz_question_new_question_not_allowed(self):
        res = self.client().get("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()