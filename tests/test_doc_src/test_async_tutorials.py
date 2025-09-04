import pytest

from tests.test_doc_src.conftest import SETUP_TEST_DATABASE


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_sync_example():
    from docs_src.async_tutorial import sync_example

    sync_example.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_async_example():
    from docs_src.async_tutorial import async_example

    async_example.main()
