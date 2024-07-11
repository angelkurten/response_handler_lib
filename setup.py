from setuptools import setup, find_packages

setup(
    name='response_handler_lib',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/angerlkurten/response_handler',
    license='MIT',
    author='Angel Kürten',
    author_email='angel@angelkurten.com',
    description='A package for handling responses with potential errors and generic data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
