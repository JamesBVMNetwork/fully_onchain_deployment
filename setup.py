import setuptools
from src.version import __version__

setuptools.setup(
    name="onchain-deployment",
    version=__version__,
    author="EternalAI",
    description="Toolkit to deploy model onchain",
    long_description="Toolkit to deploy model from Keras to onchain",
    long_description_content_type="text",
    license='LICENSE.txt',
    packages=setuptools.find_packages(),
    classifiers=['Operating System :: POSIX', ],
    entry_points={
        'console_scripts': [
            'eai = src.cli:main',
        ]
    }
)
