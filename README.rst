===============================
    django-admin-customizer
===============================

Django admin customizing interface

.. note::

    In development ...

    Implementation plan:

    * models - done
    * generator for models (as management command) - done
    * configration ui - done
    * sorting fields in configuration ui - pending
    * modeladmin factory - pending
    * dynamic url dispatch to managed modeladmins - pending
    * actions configurator - pending
    *

Features (current plan)
=======================

* Multiple admin instances for the same model
* Customization of:

  * list_display
  * list_filter
  * raw_id_fields
  * actions
  * search_fields

Requirements
============

* Django (versions tbd - maybe >= 1.3)


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

You need to update ``admin_customizer``'s models to get it working, initially and
after each model change with::

    manage.py refresh_available_fields

.. note::

    If you delete models the registered admins will be deleted for them.

    If you delete fields from models the registered admins will have them
    removed after you run refresh_available_fields.

``django-admin-customizer`` has static files for widgets in the edit interface.
If you use staticfiles just run::

    manage.py collectstatic

If you do not use django.contrib.staticfiles you must manually symlink the
site-packages/admin_customizer/static/admin_customizer dir to <your media root>/admin_customizer.

Making extra actions available
==============================

Settings
========

``ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH`` - depth to look for relations when
inspecting models.

Screenshots
===========

Edit page:

.. image:: https://github.com/downloads/ionelmc/django-admin-customizer/asdf
