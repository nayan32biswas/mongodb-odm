import pytest

from tests.test_doc_src.conftest import SETUP_TEST_DATABASE


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_overview():
    from docs_src import overview  # noqa
