import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock runpod and crewai dependencies before importing handler
sys.modules['runpod'] = MagicMock()
sys.modules['crewai'] = MagicMock()
sys.modules['crewai.tools'] = MagicMock()

# Now we can safely import handler
# Add the parent directory to sys.path to import handler
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handler import handler, create_blog_post

class TestHandler(unittest.TestCase):
    @patch('handler.create_blog_post')
    def test_handler_happy_path(self, mock_create_blog_post):
        # Setup mock
        mock_create_blog_post.return_value = "This is a mock blog post about AI."

        # Test input
        job = {"input": {"topic": "AI"}}

        # Call handler
        result = handler(job)

        # Assertions
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["blog_post"], "This is a mock blog post about AI.")
        mock_create_blog_post.assert_called_once_with("AI")

    @patch('handler.create_blog_post')
    def test_handler_default_topic(self, mock_create_blog_post):
        # Setup mock
        mock_create_blog_post.return_value = "This is a mock blog post about technology."

        # Test input with missing topic
        job = {"input": {}}

        # Call handler
        result = handler(job)

        # Assertions
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["blog_post"], "This is a mock blog post about technology.")
        mock_create_blog_post.assert_called_once_with("technology")

    @patch('handler.create_blog_post')
    def test_handler_error_path(self, mock_create_blog_post):
        # Setup mock to raise an exception
        mock_create_blog_post.side_effect = Exception("CrewAI processing failed")

        # Test input
        job = {"input": {"topic": "Error Topic"}}

        # Call handler
        result = handler(job)

        # Assertions
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "CrewAI processing failed")
        mock_create_blog_post.assert_called_once_with("Error Topic")

    @patch('handler.Crew')
    @patch('handler.Task')
    def test_create_blog_post(self, mock_task, mock_crew):
        # Setup mock crew and kickoff result
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance

        mock_result = MagicMock()
        mock_result.raw = "Raw blog post content"
        mock_crew_instance.kickoff.return_value = mock_result

        # Call create_blog_post
        result = create_blog_post("Machine Learning")

        # Assertions
        self.assertEqual(result, "Raw blog post content")
        mock_crew_instance.kickoff.assert_called_once()
        mock_crew.assert_called_once()

if __name__ == '__main__':
    unittest.main()
