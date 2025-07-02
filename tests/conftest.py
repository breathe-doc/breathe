from __future__ import annotations

import pathlib

import pytest

# Register sphinx fixtures
#
# Disable ruff warnings about unused imports as the import is the registration (I think)
from sphinx.testing.fixtures import (
    app_params,  # noqa: F401
    make_app,  # noqa: F401
    rootdir,  # noqa: F401
    shared_result,  # noqa: F401
    sphinx_test_tempdir,  # noqa: F401
    test_params,  # noqa: F401
)


# Disable ruff warnings about unused arguments as they are there by convention (I assume)
@pytest.fixture
def app(test_params, app_params, make_app, shared_result):  # noqa: F811
    """
    Based on sphinx.testing.fixtures.app
    """
    args, kwargs = app_params
    assert "srcdir" in kwargs
    pathlib.Path(kwargs["srcdir"]).mkdir(parents=True, exist_ok=True)
    (kwargs["srcdir"] / "conf.py").write_text("", encoding="utf-8")
    app_ = make_app(*args, **kwargs)
    yield app_

    print("# testroot:", kwargs.get("testroot", "root"))
    print("# builder:", app_.builder.name)
    print("# srcdir:", app_.srcdir)
    print("# outdir:", app_.outdir)
    print("# status:", "\n" + app_._status.getvalue())
    print("# warning:", "\n" + app_._warning.getvalue())

    if test_params["shared_result"]:
        shared_result.store(test_params["shared_result"], app_)
