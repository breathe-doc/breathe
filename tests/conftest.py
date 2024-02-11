import pathlib
import pytest
from sphinx.testing.fixtures import (
    test_params,
    app_params,
    make_app,
    shared_result,
    sphinx_test_tempdir,
    rootdir,
)


@pytest.fixture(scope="function")
def app(test_params, app_params, make_app, shared_result):
    """
    Based on sphinx.testing.fixtures.app
    """
    args, kwargs = app_params
    assert "srcdir" in kwargs
    pathlib.Path(kwargs["srcdir"]).mkdir(parents=True, exist_ok=True)
    (kwargs["srcdir"] / "conf.py").write_text("")
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
