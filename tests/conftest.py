"""
Pytest fixtures for integration tests.

This module defines pytest fixtures that are used across multiple integration
test files. Fixtures provide a fixed baseline upon which tests can reliably
and repeatedly execute. The fixtures defined here are for managing the lifecycle
of a test HTTP server.
"""

import pytest

from tests.helpers.server_manager import TestServer


@pytest.fixture(scope="session")
def test_server():
    """
    A pytest fixture that starts and stops a test HTTP server.

    This fixture has a "session" scope, meaning it will start the server once
    before any tests in the session are run, and stop it after all tests in the
    session have completed. It yields the TestServer instance to the tests.
    """
    server = TestServer()
    server.start()
    yield server
    server.stop()
