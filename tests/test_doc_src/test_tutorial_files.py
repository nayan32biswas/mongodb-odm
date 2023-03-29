from ..conftest import init_config  # noqa


def test_create():
    from docs_src.tutorial.create.tutorial000 import main  # noqa

    main()


def test_indexes():
    from docs_src.tutorial.indexes import tutorial000, tutorial001

    tutorial000.main()
    tutorial001.main()


def test_find_and_filter():
    from docs_src.tutorial.find_and_filter import tutorial000

    tutorial000.main()


def test_find_and_sort():
    from docs_src.tutorial.find_and_sort import tutorial000

    tutorial000.main()


def test_find_limit_and_skip():
    from docs_src.tutorial.find_limit_and_skip import tutorial000

    tutorial000.main()


def test_find_one_document():
    from docs_src.tutorial.find_one_document import tutorial000

    tutorial000.main()


def test_get_document():
    from docs_src.tutorial.get_document import tutorial000

    tutorial000.main()


def test_get_or_create():
    from docs_src.tutorial.get_or_create import tutorial000

    tutorial000.main()


def test_find_raw():
    from docs_src.tutorial.find_raw import tutorial000

    tutorial000.main()


def test_aggregate():
    from docs_src.tutorial.aggregate import tutorial000

    tutorial000.main()


def test_update():
    from docs_src.tutorial.update import tutorial000

    tutorial000.main()


def test_delete():
    from docs_src.tutorial.delete import tutorial000

    tutorial000.main()
