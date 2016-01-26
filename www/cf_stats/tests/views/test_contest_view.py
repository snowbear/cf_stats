from django.test import TestCase
from unittest.mock import patch, Mock


class Test(TestCase):
    def setUp(self):
        super().setUp()
        self.contest_id = 5

    def get_view_response(self):
        return self.client.get('/contest/' + str(self.contest_id))

    @patch('cf_stats.views.FileStorage')
    def test_contest_data_np_present(self, file_storage):
        file_content = "some text"

        file_storage.get_contest_stats = Mock(return_value=file_content)

        response = self.get_view_response()

        file_storage.get_contest_stats.assert_called_once_with(self.contest_id)

        self.assertEqual(response.content, file_content.encode('utf-8'))

    @patch('cf_stats.views.FileStorage')
    def test_contest_data_not_present(self, file_storage):
        file_storage.get_contest_stats = Mock(return_value=None)

        response = self.get_view_response()

        self.assertTemplateUsed(response, 'cf_stats/contest_data_not_present.html')
