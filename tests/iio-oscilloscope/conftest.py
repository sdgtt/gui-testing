def pytest_addoption(parser):
    parser.addoption(
        "--osc-path",
        action="store",
        default="",
        help="Path to IIO Oscilloscope executable",
    )
