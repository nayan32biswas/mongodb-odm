from .conftest import setup_test_database  # noqa


def test_overview(setup_test_database):  # noqa
    from docs_src import overview  # noqa
