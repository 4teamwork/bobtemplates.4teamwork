from ftw.bob.templates.cli import AVAILABLE_TEMPLATES
from ftw.bob.templates.cli import test_template
from unittest2 import TestCase


class TestTemplates(TestCase):

    def test_template_tests(self):
        for template_name in AVAILABLE_TEMPLATES.keys():
            args = [template_name]
            test_template(args)
