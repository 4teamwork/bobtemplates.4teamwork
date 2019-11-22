from setuptools import setup, find_packages
import os


extras_require = {
    'test': [
    ],
}

setup(name='bobtemplates.4teamwork',
      version='1.0.0.dev0',
      author='4teamwork AG',
      url='https://github.com/4teamwork/bobtemplates.4teamwork',
      description="Webpolicy generator with mr.bob template.",
      long_description=open("README.rst").read(),
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'setuptools',
          'mr.bob',
          'nose',
          'nose-selecttests',
          'nose-parameterized',
          'requests',
      ],

      tests_require=extras_require['test'],
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      create = cli:main
      template_test = cli:template_test
      fulltest = cli:fulltest
      autogenerate = cli:autogenerate
      buildout_template = cli:buildout_template
      update_lawgiver_workflow = cli:update_lawgiver_workflow
      """,
      )
