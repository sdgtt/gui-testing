import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--remote",
        action="store_true",
        help="Run test on network mode",
    )

    parser.addoption(
        "--local",
        action="store_true",
        help="Run test on local mode",
    )

    parser.addoption(
        "--ip",
        action="store",
        default="localhost",
        help="IP of DUT",
    )

    parser.addoption(
        "--delay",
        action="store",
        type=int,
        default=10,
        help="adding delay or sleep time",
    )


def pytest_configure(config):
    # register marker
    config.addinivalue_line("markers", "remote: mark remote tests")
    config.addinivalue_line("markers", "local: mark local tests")


def pytest_runtest_setup(item):
    remote = item.config.getoption("--remote")
    marks = [mark.name for mark in item.iter_markers()]
    if not remote and "remote" in marks:
        pytest.skip(
            "Testing requires network flag: --remote"
        )

    local = item.config.getoption("--local")
    marks = [mark.name for mark in item.iter_markers()]
    if not local and "local" in marks:
        pytest.skip(
            "Testing requires local flag: --local"
        )

@pytest.fixture(scope="session")
def ip(pytestconfig):
    return pytestconfig.getoption("ip")


@pytest.fixture(scope="session")
def delay(pytestconfig):
    return pytestconfig.getoption("delay")