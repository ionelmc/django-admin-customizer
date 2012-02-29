===============================
    django-admin-customizer
===============================


Django admin customizing interface

Features
========

* Multiple admin instances for the same model
* Customization of:

  * list_display
  * list_filter
  * raw_id_fields
  * actions
  * search_fields

Requirements
============

* Django (versions tbd)


Installation guide
==================

Install from pypi, with pip::

    pip install django-admin-customizer

Or with setuptools::

    easy_install django-admin-customizer

Add ``admin_customizer`` to ``INSTALLED_APPS``::

    INSTALLED_APPS += ("admin_customizer", )

After that you need to run::

    manage.py syncdb

Or if you use south::

    manage.py syncdb --migrate

..note ::

    You need to run syndb/migrate after each model change to have the admins and
    customization interface working.

``django-admin-customizer`` has static files for widgets in the edit interface.
If you use staticfiles just run::

    manage.py collectstatic

If you do not use django.contrib.staticfiles you must manually symlink the
site-packages/admin_customizer/static/admin_customizer dir to <your media root>/admin_customizer.

Making extra actions available
==============================

Settings
========

Screenshots
===========

Edit page:

.. image:: https://github.com/downloads/ionelmc/xxx
