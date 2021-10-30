from django.test import TestCase
from django.urls import reverse
from django.urls.base import resolve

from ..views import HomeView,TopicsView
from ..models import Board

# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Testing Board", description="Board for Django testing purpose")
        url = reverse("home")
        self.response = self.client.get(url)

    def test_home_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_HomeView(self):
        view = resolve("/")
        self.assertEqual(view.func, HomeView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

class BoardTopicsTest(TestCase):
    """
    This is test for Topics
    """

    def setUp(self):
        """
        This create temporary board for testing 
        """
        Board.objects.create(name="Testing Board", description="Board for Django testing purpose")
    
    def test_board_topics_view_sucess_status_code(self):
        """
        This function gets status code 200(success) for existing board 
        """       
        url = reverse("topics", kwargs={"pk":1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        """
        This function gets status code 404(page not found) for non existing board 
        """     
        url = reverse("topics",kwargs={"pk":99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        """
        This function testing correct view funcion to render topics
        """ 
        view = resolve("/boards/1/")
        self.assertEqual(view.func,TopicsView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewTopicsTests(TestCase):
    def setUp(self):
        """
        This create temporary board for testing 
        """
        Board.objects.create(name="Testing Board", description="Board for Django testing purpose")
    
    def test_new_topic_view_sucess_status_code(self):
        """
        This function gets status code 200(success) for existing topic 
        """       
        url = reverse("new_topic", kwargs={"pk":1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        """
        This function gets status code 404(page not found) for non existing topic 
        """     
        url = reverse("new_topic",kwargs={"pk":99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topics_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse("new_topic", kwargs={'pk': 1})
        board_topic_url = reverse("topics", kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topic_url))