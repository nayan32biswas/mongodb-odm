from mongodb_odm import disconnect


def test_model_inheritance():
    disconnect()
    from docs_src.advanced_tutorial.model_inheritance import tutorial000

    tutorial000.main()


def test_multiple_database():
    disconnect()
    from docs_src.advanced_tutorial.multiple_database import tutorial000

    tutorial000.main()
