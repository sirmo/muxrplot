
import pip

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = "Python rulez"

links = []  # for repo urls (dependency_links)
requires = ['numpy']  # for package names

try:
    requirements = pip.req.parse_requirements('requirements.txt', session=False)
except:
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements(
        'requirements.txt', session=pip.download.PipSession()
    )

for item in requirements:
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None):  # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))  # always the package name

setup(
    name='Muxr Plot',
    version="0.0.1",
    url='https://github.com/sirmo/mplot',
    license='MIT',
    author="Muxr",
    author_email="nospam@nospam.nocom",
    description='Capturing and plotting metrology measurements from digital bench DMMs',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    dependency_links=links,
    entry_points={
        "console_scripts": [
            "mplotlogger = mplot.logger:main",
            "mplot = mplot.plot:main",
        ]
    },
)
