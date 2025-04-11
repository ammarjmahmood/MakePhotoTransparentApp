from setuptools import setup

setup(
    name="transparent-bg",
    version="1.0.0",
    description="Remove background from images via right-click menu",
    author="Your Name",
    packages=[],
    install_requires=[
        'opencv-python>=4.5.0',
        'numpy>=1.19.0',
        'onnxruntime>=1.8.0',
        'Pillow>=8.0.0',
    ],
) 