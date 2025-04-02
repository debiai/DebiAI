from setuptools import setup, find_packages
from debiaiServer.utils.utils import get_app_version

try:
    VERSION = get_app_version()
except ModuleNotFoundError:
    VERSION = "0.0.0"

setup(
    name="debiai-gui",
    version=VERSION,
    packages=find_packages(include=["debiaiServer", "debiaiServer.*"]),
    include_package_data=True,
    install_requires=[
        "Flask==2.0.3",
        "flask_cors==3.0.8",
        "connexion==2.6.0",
        "requests==2.25.1",
        "swagger-ui-bundle==0.0.5",
        "ujson==5.8.0",
        "kafka-python==2.0.2",
        "openapi_spec_validator==0.2.8",
        "PyYAML==6.0",
        "cacheout==0.14.1",
        "termcolor==2.3.0",
        "werkzeug==2.2.2",
        "psutil==6.0.0",
        "waitress==3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "debiai-gui=debiaiServer.debiai_gui_utils:main",
        ],
    },
    author="IRT-Systemx",
    author_email="debiai@irt-systemx.fr",
    description="DebiAI easy start module, the standalone version of DebiAI",
    long_description=open("debiai_gui.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/debiai/DebiAI",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
