from mongodb_odm.connection import disconnect


def test_overview():
    disconnect()
    from docs_src import overview  # noqa
