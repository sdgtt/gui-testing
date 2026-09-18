def pytest_addoption(parser):
    parser.addoption(
        "--scopy-path",
        action="store",
        default="",
        help="Path to Scopy executable",
    )
