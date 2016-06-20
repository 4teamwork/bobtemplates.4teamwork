from setuptools import setup, find_packages
import os


extras_require = {
    'tests': [
        'ftw.testing',
        'plone.app.testing',
        'unittest2',
    ],
}

setup(name='ftw.bob.templates',
      version='1.0.0.dev0',
      author='4teamwork AG',
      url='https://github.com/4teamwork/ftw.bob.templates',
      description="Webpolicy generator with mr.bob template.",
      long_description=open("README.rst").read(),
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.bob'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'setuptools',
          'mr.bob',
      ],

      tests_require=extras_require['tests'],
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      create = ftw.bob.templates.cli:main
      test_template = ftw.bob.templates.cli:test_template
      fulltest = ftw.bob.templates.cli:fulltest
      autogenerate = ftw.bob.templates.cli:autogenerate
      buildout_template = ftw.bob.templates.cli:buildout_template
      update_lawgiver_workflow = ftw.bob.templates.cli:update_lawgiver_workflow
      """,
      )
