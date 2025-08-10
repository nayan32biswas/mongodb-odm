import pytest

from tests.test_doc_src.conftest import SETUP_TEST_DATABASE


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_model_inheritance():  # noqa
    from docs_src.advanced_tutorial.multiple_database.tutorial000 import Log

    # To fix test we have make the Log db name to None instead of "logging"
    Log.ODMConfig.database = None  # type: ignore

    from docs_src.advanced_tutorial.model_inheritance import tutorial000

    tutorial000.main()


@pytest.mark.usefixtures(SETUP_TEST_DATABASE)
def test_multiple_database():  # noqa
    from docs_src.advanced_tutorial.multiple_database.tutorial000 import Log, main

    main()

    # To fix test we have make the Log db name to None instead of "logging"
    Log.ODMConfig.database = None  # type: ignore
