import setuptools

setuptools.setup(
    name="Quadruped Controller Refactored",
    version="0.1",
    author="Nathan Kau",
    author_email="nathankau@gmail.com",
    description="Core functions for controlling quadruped robots",
    packages=["quadrupedcontroller"],
    install_requires=[
        "numpy",
        "pyyaml",
        "transforms3d",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
