from .conftest import setup_test_database  # noqa


def test_foreignkey_relationship(setup_test_database):  # noqa
    from docs_src.tutorial.relation.foreignkey_relationship import tutorial000

    tutorial000.main()


def test_many_to_many_relationship_000(setup_test_database):  # noqa
    from docs_src.tutorial.relation.many_to_many_relationship import tutorial000

    tutorial000.main()


def test_many_to_many_relationship_001(setup_test_database):  # noqa
    from docs_src.tutorial.relation.many_to_many_relationship import tutorial001

    tutorial001.main()
