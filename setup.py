from setuptools import setup, find_packages

setup(
    name="digital_image",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "opencv-python>=4.5.0",
        "scikit-image>=0.18.0",
        "Pillow>=8.0.0",
        "scipy>=1.6.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Digital image processing project using Python",
)
