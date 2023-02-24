import setuptools

setuptools.setup(
    name="ebaysdksearch",
    version="0.0.1",
    author="aeorxc",
    author_email="author@example.com",
    description="common commodity plotting including seasonal charts using plotly",
    url="https://github.com/aeorxc/ebaysdksearch",
    project_urls={
        "Source": "https://github.com/aeorxc/ebaysdksearch",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "ebaysdk",
        "requests",
        "python-dotenv",
    ],
    python_requires=">=3.9",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
