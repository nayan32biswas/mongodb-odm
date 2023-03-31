from ..conftest import init_config  # noqa


def test_foreignkey_relationship():
    from docs_src.tutorial.relation.foreignkey_relationship import tutorial000

    tutorial000.main()


def test_many_to_many_relationship():
    from docs_src.tutorial.relation.many_to_many_relationship import (
        tutorial000,
        tutorial001,
    )

    tutorial000.main()
    tutorial001.main()