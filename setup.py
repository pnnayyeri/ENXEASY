import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ENXEASY",
    version="1.0",
    author="Pooyan Nayyeri",
    author_email="pnnayyeri@gmail.com",
    description="ENX EASY absolute rotary encoders library for Raspberry Pi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pnnayyeri/ENXEASY",
    packages=setuptools.find_packages(),
    install_requires=['RPi.GPIO', 'graycode'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    keywords = [
        "raspberrypi",
        "encoder",
        "gpio",
        "absolute",
        "rotary"
    ]
)
