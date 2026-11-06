import setuptools
setuptools.setup(
    name="pre-resize",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Resize - Preprocessing Component for NOVAVISION",
    url='https://github.com/novavision-ai/pre-resize',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless', 'numpy'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        'pre.resize',
        'pre.resize.executors',
        'pre.resize.models',
        'pre.resize.utils'
    ],
    package_dir={'pre.resize': 'src'},
    python_requires=">=3.6"
)
