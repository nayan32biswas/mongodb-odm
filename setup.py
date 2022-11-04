import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='mongodb-odm',
    version='0.1-alpha2',
    description='This is a minimal ODM for MongoDB. Build top of pymongo and pydantic.',
    long_description=README,
    url='https://github.com/nayan32biswas/mongodb-odm',
    author='Nayan Biswas',
    author_email='nayan32biswas@gmail.com',
    license='MIT License',  # example license
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    # Keywords that define your package best
    keywords=['mongodb', 'mongo', 'odm', 'mongodb odm',
              'pymongo', 'pymongo odm', 'pydantic', 'pydantic odm'],
    install_requires=['pymongo', 'pydantic'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
