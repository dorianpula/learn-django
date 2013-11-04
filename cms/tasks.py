#!/usr/bin/python

# A quick and dirty task setup to play around with invoke
from invoke import task, run


@task
def runserver(debug=False):
    """Convenience command for running a test server."""

    base_command = "python manage.py runserver{}"
    if debug:
        base_command = base_command.format("_plus")
    else:
        base_command = base_command.format("")

    run(base_command)