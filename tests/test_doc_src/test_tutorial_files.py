import pytest

from tests.test_doc_src.conftest import SETUP_TEST_DATABASE


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_create():
    from docs_src.tutorial.create import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_indexes_000():
    from docs_src.tutorial.indexes import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_indexes_001():
    from docs_src.tutorial.indexes import tutorial001

    tutorial001.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_find_and_filter():
    from docs_src.tutorial.find_and_filter import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_find_and_sort():
    from docs_src.tutorial.find_and_sort import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_find_limit_and_skip():
    from docs_src.tutorial.find_limit_and_skip import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_find_one_document():
    from docs_src.tutorial.find_one_document import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_get_document():
    from docs_src.tutorial.get_document import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_get_or_create():
    from docs_src.tutorial.get_or_create import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_find_raw():
    from docs_src.tutorial.find_raw import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_aggregate():
    from docs_src.tutorial.aggregate import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_update():
    from docs_src.tutorial.update import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_delete():
    from docs_src.tutorial.delete import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_transaction():
    from docs_src.tutorial.transaction import tutorial000

    tutorial000.main()
