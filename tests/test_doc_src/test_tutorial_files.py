from .conftest import setup_test_database  # noqa


def test_create(setup_test_database):  # noqa
    from docs_src.tutorial.create import tutorial000

    tutorial000.main()


def test_indexes_000(setup_test_database):  # noqa
    from docs_src.tutorial.indexes import tutorial000

    tutorial000.main()


def test_indexes_001(setup_test_database):  # noqa
    from docs_src.tutorial.indexes import tutorial001

    tutorial001.main()


def test_find_and_filter(setup_test_database):  # noqa
    from docs_src.tutorial.find_and_filter import tutorial000

    tutorial000.main()


def test_find_and_sort(setup_test_database):  # noqa
    from docs_src.tutorial.find_and_sort import tutorial000

    tutorial000.main()


def test_find_limit_and_skip(setup_test_database):  # noqa
    from docs_src.tutorial.find_limit_and_skip import tutorial000

    tutorial000.main()


def test_find_one_document(setup_test_database):  # noqa
    from docs_src.tutorial.find_one_document import tutorial000

    tutorial000.main()


def test_get_document(setup_test_database):  # noqa
    from docs_src.tutorial.get_document import tutorial000

    tutorial000.main()


def test_get_or_create(setup_test_database):  # noqa
    from docs_src.tutorial.get_or_create import tutorial000

    tutorial000.main()


def test_find_raw(setup_test_database):  # noqa
    from docs_src.tutorial.find_raw import tutorial000

    tutorial000.main()


def test_aggregate(setup_test_database):  # noqa
    from docs_src.tutorial.aggregate import tutorial000

    tutorial000.main()


def test_update(setup_test_database):  # noqa
    from docs_src.tutorial.update import tutorial000

    tutorial000.main()


def test_delete(setup_test_database):  # noqa
    from docs_src.tutorial.delete import tutorial000

    tutorial000.main()


def test_transaction(setup_test_database):  # noqa
    from docs_src.tutorial.transaction import tutorial000

    tutorial000.main()
