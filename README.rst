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
  * search_fields

TODO
====

* actions configurator
* base admin class support

Requirements
============

* Django 1.2, 1.3, 1.4, trunk. Django 1.1 is NOT supported.
* Python 2.6 or 2.7

.. image:: https://secure.travis-ci.org/ionelmc/django-admin-customizer.png
    :alt: Build Status
    :target: http://travis-ci.org/ionelmc/django-admin-customizer

Installation guide
==================

Install from pypi, with pip::

    pip install django-admin-customizer

Or with setuptools::

    easy_install django-admin-customizer

Add ``admin_customizer`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS += ("admin_customizer", )

Add the admin customizer's urls to your root url conf. This is the url where
your will access your custom admin instances. Eg: in your project's urls.py add:

.. code-block:: python

    (r'^admin/_/', include('admin_customizer.urls')),

After that you need to run::

    manage.py syncdb

Or if you use south::

    manage.py syncdb --migrate

You need to update ``admin_customizer``'s models to get it working, initially and
after each model change with::

    manage.py refresh_available_fields

**Note:**

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

*TODO*

Settings
========

``ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH`` - depth to look for relations when
inspecting models.

Middleware
==========

To enable urlpattern reloading add
``'admin_customizer.middleware.URLResolverReloadMiddleware'`` to
``MIDDLEWARE_CLASSES``.

**Warning!**

    You must have working django cache for this to work properly ! See django's
    `cache documentation
    <https://docs.djangoproject.com/en/dev/topics/cache/#setting-up-the-cache>`_
    on this.

If you do not enable this you will have to restart the webserver after every
AdminSite or RegisteredModel change !


Screenshots
===========

Edit page:

.. image:: https://github.com/downloads/ionelmc/django-admin-customizer/admin-customizer-registered-model-edit-page.png
