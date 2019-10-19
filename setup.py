import setuptools

setuptools.setup(
    name='cstore',
    version='1.0',
    description='Component Store Command Line Client',
    packages=setuptools.find_packages(),
    scripts=['bin/cstore'],
    url='https://github.com/tehyulekim/Capstone',
    author='Teh Yule Kim',
    author_email='tehyulekim@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
    zip_safe=False,
    install_requires=[
        'fire',
        'requests'
    ],
)
