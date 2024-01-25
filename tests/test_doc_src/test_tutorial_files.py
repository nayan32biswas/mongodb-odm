from mongodb_odm import disconnect


def test_create():
    disconnect()
    from docs_src.tutorial.create import tutorial000

    tutorial000.main()


def test_indexes():
    disconnect()
    from docs_src.tutorial.indexes import tutorial000, tutorial001

    tutorial000.main()
    tutorial001.main()


def test_find_and_filter():
    disconnect()
    from docs_src.tutorial.find_and_filter import tutorial000

    tutorial000.main()


def test_find_and_sort():
    disconnect()
    from docs_src.tutorial.find_and_sort import tutorial000

    tutorial000.main()


def test_find_limit_and_skip():
    disconnect()
    from docs_src.tutorial.find_limit_and_skip import tutorial000

    tutorial000.main()


def test_find_one_document():
    disconnect()
    from docs_src.tutorial.find_one_document import tutorial000

    tutorial000.main()


def test_get_document():
    disconnect()
    from docs_src.tutorial.get_document import tutorial000

    tutorial000.main()


def test_get_or_create():
    disconnect()
    from docs_src.tutorial.get_or_create import tutorial000

    tutorial000.main()


def test_find_raw():
    disconnect()
    from docs_src.tutorial.find_raw import tutorial000

    tutorial000.main()


def test_aggregate():
    disconnect()
    from docs_src.tutorial.aggregate import tutorial000

    tutorial000.main()


def test_update():
    disconnect()
    from docs_src.tutorial.update import tutorial000

    tutorial000.main()


def test_delete():
    disconnect()
    from docs_src.tutorial.delete import tutorial000

    tutorial000.main()


def test_transaction():
    disconnect()
    from docs_src.tutorial.transaction import tutorial000

    tutorial000.main()
