from setuptools import setup

setup(
    packages=['medmij'],
    zip_safe=True,
    test_suite='nose.collector',
    tests_require=['nose'],
)
