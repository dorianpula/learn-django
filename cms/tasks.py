#!/usr/bin/python

# A quick and dirty task setup to play around with invoke
from invoke import task, run


@task(help={"debug": "Run the server in debug mode."})
def run_server(debug=False):
    """Convenience command for running a test server.
       
       :param debug: Whether or not to run as in debug mode.
    """

    base_command = "python manage.py runserver{}"
    if debug:
        base_command = base_command.format("_plus")
    else:
        base_command = base_command.format("")

    run(base_command)
