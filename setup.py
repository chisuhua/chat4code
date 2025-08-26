from setuptools import setup, find_packages

setup(
    name="chat4code",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="让代码与AI对话更简单",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chat4code",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyYAML>=5.0",
    ],
    entry_points={
        "console_scripts": [
            "chat4code=chat4code.cli:main",
        ],
    },
)
