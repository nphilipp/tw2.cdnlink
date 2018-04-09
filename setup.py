from setuptools import setup, find_packages

requires = ["tw2.core >= 2.0"]

_extra_genshi = ["Genshi >= 0.3.5"]
_extra_mako = ["Mako >= 0.1.1"]
_extra_jinja = ["Jinja2"]

tests_require = [
    "nose",
    "sieve",
    "coverage",
    "webtest"] + _extra_genshi + _extra_mako + _extra_jinja


if __name__ == '__main__':
    setup(
        name='tw2.cdnlink',
        version='0.1',
        description="ToscaWidgets 2 extension for CDN resources",
        author="Nils Philippsen",
        author_email="nils@tiptoe.de",
        #url=
        #download_url=
        setup_requires=[],
        install_requires=["tw2.core >= 2.0"],
        packages=find_packages(exclude=["tests"]),
        namespace_packages=['tw2'],
        zip_safe=True,
        test_suite='nose.collector',
        tests_require=tests_require,
        extras_require={
            'genshi': _extra_genshi,
            'mako': _extra_mako,
            'jinja': _extra_jinja,
            'test': tests_require,
            'tests': tests_require,
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Web Environment",
            "Environment :: Web Environment :: ToscaWidgets",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Widget Sets",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
        ]
    )
