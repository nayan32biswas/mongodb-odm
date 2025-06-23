import pytest

from tests.test_doc_src.conftest import SETUP_TEST_DATABASE


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_foreignkey_relationship():
    from docs_src.tutorial.relation.foreignkey_relationship import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_many_to_many_relationship_000():
    from docs_src.tutorial.relation.many_to_many_relationship import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_many_to_many_relationship_001():
    from docs_src.tutorial.relation.many_to_many_relationship import tutorial001

    tutorial001.main()
