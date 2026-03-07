"""
Pipeline Safety AI Evaluator (PSAE) - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path) as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="pipeline-safety-ai-evaluator",
    version="1.0.0",
    author="Pipeline AI Solutions LLC",
    author_email="research@pipelinegpt.ai",
    description="A PhD-level evaluation framework for AI systems in pipeline safety-critical applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pipelinegpt/psae",
    project_urls={
        "Bug Tracker": "https://github.com/pipelinegpt/psae/issues",
        "Documentation": "https://pipelinegpt.ai/psae/docs",
        "Source": "https://github.com/pipelinegpt/psae",
    },
    packages=find_packages(where="src"),
    py_modules=["cli"],
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    keywords="ai evaluation safety pipeline gas utilities engineering assessment",
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.3.0",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "flake8>=6.0.0",
            "mypy>=1.3.0",
            "sphinx>=7.0.0",
        ],
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.8.0"],
        "google": ["google-generativeai>=0.3.0"],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.8.0",
            "google-generativeai>=0.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "psae=psae.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
