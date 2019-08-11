import io
import re

from setuptools import setup, find_packages

with io.open('pymiddy/__init__.py', 'rt', encoding='utf8') as f:
    file_content = f.read()
    name = re.search(r"__name__ = '(.*?)'", file_content).group(1)
    version = re.search(r"__version__ = '(.*?)'", file_content).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

    setup(name=name,
          version=version,
          description='Middleware engine for AWS Lambda - Inspired by middyjs',
          url='https://github.com/godvsdeity/pymiddy',
          author='Alex Pasare',
          author_email='alexandru.pasare@simplecoding.email',
          long_description=long_description,
          long_description_content_type="text/markdown",
          license='MIT',
          packages=find_packages(),
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ],
          zip_safe=False)
