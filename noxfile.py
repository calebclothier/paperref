import nox


@nox.session
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python="3.11")
def tests(session: nox.Session) -> None:
    """
    Run the tests.
    """
    session.cd("backend")
    session.install(".[test]")
    session.run("pytest", *session.posargs)
