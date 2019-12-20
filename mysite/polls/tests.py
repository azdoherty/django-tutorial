from django.test import TestCase
from django.utils import timezone   
from django.urls import reverse
import datetime

from .models import Question

def create_question(question_text, days):
    """
    create a question with a pub date offset from now by days
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_new_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        new_question = Question(pub_date=time)
        self.assertIs(new_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_past_question(self):
        create_question("Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_future_and_past_question(self):
        create_question('Past question', days = -30)
        create_question('Future question', days = 30)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )


    def test_two_past_questions(self):
        create_question('Past question', days = -30)
        create_question('Past question 1', days = -60)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>', '<Question: Past question 1>']
        )

