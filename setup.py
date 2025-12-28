from setuptools import setup, find_packages

setup(
    name="enterprise_genai_platform",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "pydantic",
        "streamlit",
        "faiss-cpu",
        "neo4j",
        "openai",
        "pytest",
        "tiktoken",
        "faiss-cpu",
        "sentence-transformers",
        "openai",
        "numpy"

    ],
    entry_points={
        "console_scripts": [
            "egp-ingest=tools.cli:main",
            "egp-chunk=tools.cli:main",
        ]
    },
    python_requires=">=3.10",
)
