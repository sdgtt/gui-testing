import pytest


def pytest_addoption(parser):
    parser.addoption("--remote", action="store_true", help="Run tests in network mode")
    parser.addoption("--local", action="store_true", help="Run tests in local mode")
    parser.addoption("--ip", action="store", default="localhost", help="IP of DUT")
    parser.addoption("--delay", action="store", type=int, default=10, help="Delay between operations")
    parser.addoption("--device", action="store", default="", help="Device under test identifier")


def pytest_configure(config):
    config.addinivalue_line("markers", "remote: mark tests requiring network mode")
    config.addinivalue_line("markers", "local: mark tests requiring local mode")
    config.addinivalue_line("markers", "x11: mark tests requiring X11 display")


def pytest_runtest_setup(item):
    marks = {mark.name for mark in item.iter_markers()}

    if "remote" in marks and not item.config.getoption("--remote"):
        pytest.skip("Requires --remote flag")
    if "local" in marks and not item.config.getoption("--local"):
        pytest.skip("Requires --local flag")


@pytest.fixture(scope="session")
def ip(pytestconfig):
    return pytestconfig.getoption("ip")


@pytest.fixture(scope="session")
def delay(pytestconfig):
    return pytestconfig.getoption("delay")


@pytest.fixture(scope="session")
def device(pytestconfig):
    return pytestconfig.getoption("device")
