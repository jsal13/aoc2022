import os

from invoke import task

# NOTE:  Type-Hinting is not able to be used until
# https://github.com/pyinvoke/invoke/issues/357 is # closed.


@task
def docs(context):  # type: ignore
    """Generate Sphinx documentation."""
    if os.name == "nt":  # if windows...
        context.run(".\\docs\\make.bat html")
    else:
        context.run("cd docs && make html && cd ..")


@task
def test(context):  # type: ignore
    """Run Pytest."""
    context.run("pytest --cov=aoc2022 tests/")


@task
def tox(context):  # type: ignore
    """Run Tox."""
    context.run("tox")
