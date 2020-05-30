from setuptools import setup, find_packages

setup(
    name="zephyr_client",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/tocehka/zephyr_client",
    author="tocehka",
    install_requires=[
        "pygatt==4.0.5",
        "numpy>=1.18.2",
        "python-socketio>=4.6.0",
        "python-dotenv>=0.13.0"
    ]
)
