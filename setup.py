from setuptools import find_packages, setup

setup(
    name="sclogging",
    version="0.0.40",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"sclogging": ["config.py", "settings.toml"]},
    url="",
    license="",
    author="",
    author_email="",
    description="",
)
