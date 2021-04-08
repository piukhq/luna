import pytest

from app.settings import to_bool


def test_to_bool() -> None:
    assert to_bool(True) is True
    assert to_bool("True") is True

    with pytest.raises(KeyError):
        to_bool("invalid")
