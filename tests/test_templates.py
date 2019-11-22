from nose_parameterized import parameterized
from unittest import TestCase
import cli


class TestTemplates(TestCase):

    @parameterized.expand(cli.AVAILABLE_TEMPLATES.keys())
    def test_template_tests(self, template_name):
        args = [template_name]
        cli.template_test(args)
