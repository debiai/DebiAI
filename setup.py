from setuptools import setup, find_packages
import os
import re


def get_version():
    """Read version from debiaiServer/swagger.yaml using regex"""
    swagger_path = os.path.join(
        os.path.dirname(__file__), "debiaiServer", "swagger.yaml"
    )
    try:
        with open(swagger_path, "r") as f:
            content = f.read()
            # Match version: "X.Y.Z" or version: X.Y.Z
            match = re.search(r'version:\s*["\']?([0-9.]+)["\']?', content)
            if match:
                return match.group(1)
            raise ValueError("Version not found in swagger.yaml")
    except (FileNotFoundError, ValueError) as e:
        raise RuntimeError(
            f"Cannot find version information in {swagger_path}. "
            "Ensure that the version is specified in the swagger.yaml file. "
            f"Error: {e}"
        ) from e


VERSION = get_version()

setup(
    name="debiai_gui",
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
        "cacheout==0.14.1",
        "termcolor==2.3.0",
        "werkzeug==2.2.2",
        "psutil==6.0.0",
        "waitress==3.0.0",
        "pickledb==1.3.2",
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
