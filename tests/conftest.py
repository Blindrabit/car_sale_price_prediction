# import pytest
# from django.test.utils import override_settings
#
#
# TEST_SETTINGS = {
#     "DEBUG": False,
# }
#
#
# @pytest.fixture(scope="session", autouse=True)
# def test_settings():
#     """
#     Fixture to override settings for testing.
#     """
#     with override_settings(**TEST_SETTINGS):
#         yield
