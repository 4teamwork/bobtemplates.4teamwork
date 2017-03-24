========================
FTW Web Policy Generator
========================

``bobtemplates.4teamwork`` generates different templates with `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ based on 4teamwork-modules.

.. contents:: Table of Contents

Installation
============

.. code:: bash

    $ git clone git@github.com:4teamwork/bobtemplates.4teamwork.git
    $ cd bobtemplates.4teamwork
    $ ln -s local.cfg buildout.cfg
    $ python2.7 bootstrap.py
    $ bin/buildout

Usage
=====

Available templates
-------------------

The following templates are available and ready to generate:

``web``
  Use this template to generate a website based on ftw.simplelayout
``workspace``
  Use this template to generate a workspace based on ftw.workspace
``module``
  Use this template if you want to start with a new ftw-module

Generating a new policy package
-------------------------------

.. code:: bash

    $ bin/create template-name

You only have to answer all the questions and your policy will be created in the ``generated`` folder.

.. image:: https://raw.github.com/4teamwork/bobtemplates.4teamwork/master/docs/flowchart-create.png

A complete documentation for deployments with ftw.bob can be found here: http://devdocs.4teamwork.ch/plone/deployment/deployment/

Development
===========

Run tests
---------

.. code:: bash

    $ bin/test

Runnig the tests of the packages will run the default package tests and also run the template tests.

To run the template-tests the test-runner will generate each template with preconfigured values and
run `bin/buildout` and `bin/test` on the template.

Helper scripts
--------------

There are several useful script provided by ``bobtemplates.4teamwork`` for development.

Test a template
~~~~~~~~~~~~~~~

If you want to test only the template you are working on, you can run

.. code:: bash

    $ bin/template_test template-name

This will autogerenate a new package based on the given template and will
run tests of this new created package.

.. image:: https://raw.github.com/4teamwork/bobtemplates.4teamwork/master/docs/flowchart-template-test.png

Autogenerate a new package
~~~~~~~~~~~~~~~~~~~~~~~~~~

To generate a package with predefined values you can use this script.

.. code:: bash

    $ bin/autogenerate template-name

.. image:: https://raw.github.com/4teamwork/bobtemplates.4teamwork/master/docs/flowchart-autogenerate.png

Generate and buildout a new package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script generates an new package and runs buildout for it.

.. code:: bash

    $ bin/buildout_package template-name

.. image:: https://raw.github.com/4teamwork/bobtemplates.4teamwork/master/docs/flowchart-buildout-package.png

Lawgiver workflow updater
-------------------------

If the template includes a generated lawgiver workflow you can use this
script to update your template workflow.

.. code:: bash

    $ bin/update_lawgiver_workflow template-name

If you do changes on the template, i.e. adding a new package in setup.py,
or if the lawgiver specifiaction.txt has changed, you would
have to recreate the  definitions.xml for the mr.bob template. That means:

- Create a package with bin/create
- Buildout it and start Zope
- Install a plonesite and generate the lawgiver workflow
- Replace all packagenames in the generated workflows to
  mr.bob variables
- Replace the workflows in the template folder with the
  generated workflows
- Do the same with the generated translations

This is a lot of stuff and is error prone.

The script is doing all this in one step for you.

.. image:: https://raw.github.com/4teamwork/bobtemplates.4teamwork/master/docs/flowchart-update-lawgiver-workflow.png

Full template test
------------------

This script is very useful if you change something on a template which
will manipulate the workflow.

It will automatically update the workflow for the template (see Lawgiver Workflow Updater),
regenerate the package and run all tests for it.

.. code:: bash

    $ bin/fulltest template-name

.. image:: https://raw.github.com/4teamwork/bobtemplates.4teamwork/master/docs/flowchart-fulltest.png

Mr. Bob
=======

See the documentation of `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_  for further information.

Flowcharts
==========

Flowcharts are created with `draw.io <https://www.draw.io/>`_
Links
=====

- Github: https://github.com/4teamwork/bobtemplates.4teamwork
- Issues: https://github.com/4teamwork/bobtemplates.4teamwork/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=bobtemplates.4teamwork

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``bobtemplates.4teamwork`` is licensed under GNU General Public License, version 2.

