from unittest2 import TestCase
import cli


class TestTemplates(TestCase):

    def test_template_tests(self):
        for template_name in cli.AVAILABLE_TEMPLATES.keys():
            args = [template_name]
            cli.template_test(args)
