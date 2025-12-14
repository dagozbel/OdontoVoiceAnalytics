"""
Setup script para OdontoVoice Analytics
Permite instalar el paquete en modo desarrollo o producción
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="OdontoVoice-Analytics",
    version="1.0.0",
    author="Diego Alberto Ortiz Beltrán",
    description="Sistema de análisis de transcripciones telefónicas para consultorios odontológicos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dagozbel/OdontoVoiceAnalytics",
    project_urls={
        "Bug Tracker": "https://github.com/dagozbel/OdontoVoiceAnalytics/issues",
        "Documentation": "https://github.com/dagozbel/OdontoVoiceAnalytics/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Healthcare :: Medical Support",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "SpeechRecognition==3.10.0",
        "pydub==0.25.1",
        "spacy==3.7.2",
        "scikit-learn==1.3.2",
        "numpy==1.24.3",
        "pydantic==2.4.2",
        "python-dotenv==1.0.0",
    ],
    extras_require={
        "api": ["flask==3.0.0", "flask-cors==4.0.0"],
        "dev": ["pytest==7.4.3", "black==23.11.0", "flake8==6.1.0"],
    },
    entry_points={
        "console_scripts": [
            "odontvoice=main:main",
        ],
    },
)
