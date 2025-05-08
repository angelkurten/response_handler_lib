from setuptools import setup, find_packages

setup(
    name='response_handler_lib',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.0.0"
    ],
    url='https://github.com/angerlkurten/response_handler_lib',
    license='MIT',
    author='Angel Kürten',
    author_email='angel@angelkurten.com',
    description='A package for handling responses with potential errors and generic data, including predefined and '
                'custom error handling. This package is used as a complement to exceptions to have more control over '
                'business logic errors.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
