import setuptools

def _get_version():
    """Extract version from package."""
    with open("pyguit/__init__.py") as reader:
        match = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', reader.read(), re.MULTILINE
        )
        if match:
            return match.group(1)
        else:
            raise RuntimeError("Unable to extract version.")

setuptools.setup(
    name="pyguit",
    version="0.0.1",
    description="Tests and testing infrastructure for GUI apps",
    url="https://github.com/sdgtt/gui-testing.git",
    author="SDG Testing Team",
    author_email="kimchesed.paller@analog.com",
    license="ADI BSD",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyvirtualdisplay",
        "pyautogui",
        "opencv-contrib-python",
        "python-xlib",
    ],
)
