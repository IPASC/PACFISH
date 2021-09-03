import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r') as requirements_file:
    requirements = requirements_file.read().splitlines()

setuptools.setup(
    name="ipasc_tool",
    version="0.1.3",
    author="International Photoacoustic Standardisation Consortium (IPASC)",
    description="Standardised Data Access Tool of IPASC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(include=["ipasc_tool", "ipasc_tool.*"]),
    install_requires=requirements,
    python_requires=">=3.7"
)
