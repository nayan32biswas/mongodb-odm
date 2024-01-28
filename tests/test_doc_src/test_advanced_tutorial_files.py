from .conftest import setup_test_database  # noqa


def test_model_inheritance(setup_test_database):  # noqa
    from docs_src.advanced_tutorial.model_inheritance import tutorial000

    tutorial000.main()


def test_multiple_database(setup_test_database):  # noqa
    from docs_src.advanced_tutorial.multiple_database import tutorial000

    tutorial000.main()
