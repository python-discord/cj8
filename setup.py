import setuptools

import project  # for version number

# To run: py setup.py sdist bdist_wheel
# To upload: py -m twine upload --sign --skip-existing dist/*
#            py -m twine upload --sign --skip-existing (--comment COMMENT) (--repository testpypi) dist/*


with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    # TODO: change name
    name='project',
    version=project.__version__,
    author='Team Cheerful Cheetahs',
    author_email='',
    license='MIT',
    description='Pending',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cj8-cheerful-cheetahs/project',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'project=project:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
    ],
    python_requires='>=3',
    install_requires=[
        '',
    ]
)
