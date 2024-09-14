from setuptools import setup, find_packages

setup(
    name='SDKAPI',
    version='0.0.1',
    description='Integration of three SDK, such as Alibaba cloud SMS.... Tencent cloud SMS... And so on',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chang hao Jiao',
    author_email='J0716gzs@163.com',
    url='https://github.com/yourusername/your_project',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your project's dependencies here.
        # e.g., 'requests', 'numpy',
    ],
    extras_require={
        'dev': [
            'pytest',
            # other development dependencies
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'your_command=your_package.module:function',
        ],
    },
)
