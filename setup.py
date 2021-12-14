import setuptools

with open('VERSION', 'r') as version_file:
    version = version_file.read()

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r') as requirements_file:
    requirements = requirements_file.read().splitlines()

setuptools.setup(
    name="pacfish",
    version=version,
    author="International Photoacoustic Standardisation Consortium (IPASC)",
    description="Photoacoustic Converter for Information Sharing (PACFISH)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    packages=setuptools.find_packages(include=["pacfish", "pacfish.*"]),
    install_requires=requirements,
    python_requires=">=3.7",
    url="https://github.com/IPASC/PACFISH/"
)
