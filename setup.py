from setuptools import setup, find_packages


extras_require = {
    'tests': [
        'plone.app.testing',
        'unittest2',
    ],
}

setup(name='ftw.bob.web',
      version='1.0.0.dev0',
      author='4teamwork AG',
      url='https://github.com/4teamwork/ftw.bob.web',
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

      entry_points={},
      )
