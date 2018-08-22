from setuptools import setup

setup(
    name='medmij',
    install_requires=['lxml'],
    packages=['medmij'],
    zip_safe=True,
    test_suite='nose.collector',
    tests_require=['nose'],
)
