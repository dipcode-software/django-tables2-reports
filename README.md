# django-tables2-reports

[![Coverage Status](https://coveralls.io/repos/github/dipcode-software/django-tables2-reports/badge.svg?branch=master)](https://coveralls.io/github/dipcode-software/django-tables2-reports?branch=master) [![Build Status](https://travis-ci.org/dipcode-software/django-tables2-reports.svg?branch=master)](https://travis-ci.org/dipcode-software/django-tables2-reports) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/77a0c6286a6443c9ad34c01af32e3fde)](https://www.codacy.com/app/srtabs/django-tables2-reports?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dipcode-software/django-tables2-reports&amp;utm_campaign=Badge_Grade)

With django-tables2-reports you can get a report (CSV, XLS) of any [table](http://pypi.python.org/pypi/django-tables2/)  with **minimal changes** to your project

Requirements
============

* [django](http://pypi.python.org/pypi/django/) (>=1.11)
* [django-tables2](http://pypi.python.org/pypi/django-tables2/) (>=1.7.1)
* [xlwt](http://pypi.python.org/pypi/xlwt/) (>=0.7.5), [openpyxl](http://pythonhosted.org/openpyxl/) (>=1.6.2) or [pyExcelerator](http://pypi.python.org/pypi/pyExcelerator/) (>=0.6.4.1) (These are optionals, to export to xls. Default to xlwt if available)


Installation
============

* In your settings:

```python
    INSTALLED_APPS = (

        'django_tables2_reports',
    )


    TEMPLATE_CONTEXT_PROCESSORS = (

        'django.core.context_processors.static',

    )


    # This is optional

    EXCEL_SUPPORT = 'xlwt' # or 'openpyxl' or 'pyexcelerator'
```

Changes in your project
=======================

1.a Now your table should extend of 'TableReport'

```python
    ############### Before ###################

    import django_tables2 as tables


    class MyTable(tables.Table):

        ...

    ############### Now ######################

    from django_tables2_reports.tables import TableReport


    class MyTable(TableReport):

        ...
```

1.b If you want to exclude some columns from report (e.g. if it is a column of buttons), you should set 'exclude_from_report' - the names of columns (as well as property 'exclude' in [table](http://pypi.python.org/pypi/django-tables2/>))

```python
    class MyTable(TableReport):

        class Meta:
            exclude_from_report = ('column1', ...)
        ...
```

2.a. If you use a traditional views, now you should use other RequestConfig and change a little your view:
```python

    ############### Before ###################

    from django_tables2 import RequestConfig


    def my_view(request):
        objs = ....
        table = MyTable(objs)
        RequestConfig(request).configure(table)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))

    ############### Now ######################

    from django_tables2_reports.config import RequestConfigReport as RequestConfig
    from django_tables2_reports.utils import create_report_http_response

    def my_view(request):
        objs = ....
        table = MyTable(objs)
        table_to_report = RequestConfig(request).configure(table)
        if table_to_report:
            return create_report_http_response(table_to_report, request)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))

```
If you have a lot of tables in your project, you can activate the middleware, and you do not have to change your views, only the RequestConfig import

```python
    # In your settings 

    MIDDLEWARE_CLASSES = (

        'django_tables2_reports.middleware.TableReportMiddleware',
    )

    ############### Now (with middleware) ######################

    from django_tables2_reports.config import RequestConfigReport as RequestConfig

    def my_view(request):
        objs = ....
        table = MyTable(objs)
        RequestConfig(request).configure(table)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))

```
2.b. If you use a [Class-based views](https://docs.djangoproject.com/en/dev/topics/class-based-views/):
```python

    ############### Before ###################

    from django_tables2.views import SingleTableView


    class PhaseChangeView(SingleTableView):
        table_class = MyTable
        model = MyModel


    ############### Now ######################

    from django_tables2_reports.views import ReportTableView


    class PhaseChangeView(ReportTableView):
        table_class = MyTable
        model = MyModel

```
Usage
=====

Under the table appear a CSV icon (and XLS icon if you have [xlwt](http://pypi.python.org/pypi/xlwt/), [openpyxl](http://pythonhosted.org/openpyxl/) or [pyExcelerator](http://pypi.python.org/pypi/pyExcelerator/) in your python path), if you click in this icon, you get a CSV report (or xls report) with every item of the table (without pagination). The ordering works!


Development
===========

You can get the last bleeding edge version of django-tables2-reports by doing a clone
of its git repository::
```python
  git clone https://github.com/dipcode-software/django-tables2-reports
```

Test project
============

In the source tree, you will find a directory called 'test_project'. It contains
a readily setup project that uses django-tables2-reports. You can run it as usual:
```python
    python manage.py syncdb --noinput
    python manage.py runserver
```
