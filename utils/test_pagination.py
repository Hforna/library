from pagination import make_range_pagination
from unittest import TestCase

class TestPagination(TestCase):
    def test_make_range_pagination(self):
        pagination = make_range_pagination(current_page=20, qty_pages=4, page_range=list(range(1, 20)))['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        