from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aura-lang",
    version="1.0.0",
    author="KingEnious",
    author_email="",
    description="Natural language programming - write code in plain English",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kingenious0/Aura-Programming-Language",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "llama-cpp-python>=0.2.0",
        "watchdog>=6.0.0",
        "requests>=2.28.0",
        "huggingface_hub>=0.16.0",
    ],
    entry_points={
        'console_scripts': [
            'aura=transpiler.cli:main',
        ],
    },
    include_package_data=True,
)
