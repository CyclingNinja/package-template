import py  # noqa: F401
import pytest

import tox  # noqa: F401
from tox.pytest import init_fixture  # noqa: F401


@pytest.fixture(params=["bake_default",
                        "bake_examples_compiled",
                        "bake_examples"])
def cookiejar(request):
    """
    All the possible renders of the template.
    """
    return request.getfixturevalue(request.param)


@pytest.fixture(params=["bake_default", ])
def cookiejar_no_examples(request):
    """
    Templates rendered without the examples
    """
    return request.getfixturevalue(request.param)


@pytest.fixture(params=["bake_examples_compiled",
                        "bake_examples",
                        "bake_examples_compiled_dev_version",
                        "bake_examples_url_extensions"])
def cookiejar_examples(request):
    """
    Templates rendered with the examples
    """
    return request.getfixturevalue(request.param)


@pytest.fixture
def baked(request):
    """
    A specific render of the template
    """
    return request.getfixturevalue(request.param)


def _handle_cookiecutter_errors(result):
    if result.exception is not None:
        raise result.exception

    assert result.exit_code == 0

    return result


@pytest.fixture
def bake_default(cookies):
    """
    Render with the defaults.
    """
    result = cookies.bake()
    return _handle_cookiecutter_errors(result)


@pytest.fixture
def bake_examples(cookies):
    """
    Examples on.
    """
    result = cookies.bake(extra_context={"include_example_code": "y",
                                         "author_name": "test",
                                         "use_extended_ruff_linting": "y"})
    return _handle_cookiecutter_errors(result)


@pytest.fixture
def bake_examples_compiled(cookies):
    """
    Examples on.
    """
    result = cookies.bake(extra_context={"include_example_code": "y",
                                         "use_compiled_extensions": "y",
                                         "author_name": "test",
                                         "use_extended_ruff_linting": "n"})
    return _handle_cookiecutter_errors(result)


@pytest.fixture
def bake_examples_compiled_dev_version(cookies):
    """
    Examples on.
    """
    result = cookies.bake(extra_context={"include_example_code": "y",
                                         "use_compiled_extensions": "y",
                                         "enable_dynamic_dev_versions": "y",
                                         "author_name": "test",
                                         "include_cruft_update_github_workflow": "y",
                                         "use_extended_ruff_linting": "y",
                                         "download_url": "https://github.com/sunpy/sunpy/archive/master.zip",
                                         "issue_tracker_url": "https://github.com/sunpy/sunpy/issues",
    })
    return _handle_cookiecutter_errors(result)


@pytest.fixture
def bake_examples_url_extensions(cookies):
    """
    setting url parameters
    """
    result = cookies.bake(extra_context={
        "author_name": "test",
        "include_example_code": "y",
        "project_url": "https://sunpy.org",
        "github_repo": "sunpy/sunpy",
        "download_url": "https://github.com/sunpy/sunpy/archive/master.zip",
        "documentation_url": "https://sunpy.org/docs",
        "changelog_url": "https://sunpy.org/changelog",
        "issue_tracker_url": "https://github.com/sunpy/sunpy/issues"
    })
    return _handle_cookiecutter_errors(result)


def pytest_addoption(parser):
    # Add support for saving out rendered cookies to a specific location for inspection
    parser.addoption("--cookie-location", action="store", default=None)
