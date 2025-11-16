import pytest

from lesekobold.src.utils.singleton import Singleton


class TestSingleton(metaclass=Singleton):
    """Test class implementing singleton pattern using Singleton metaclass."""


@pytest.mark.unit_test
def test_singleton_behavior():
    instance1 = TestSingleton()
    instance2 = TestSingleton()

    assert instance1 is instance2
