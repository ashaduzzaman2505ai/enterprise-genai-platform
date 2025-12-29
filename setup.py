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
        "tiktoken",
        "sentence-transformers",
        "numpy",
        "PyPDF2",
        "python-dotenv",
        "tqdm",
        "loguru",
        "langchain",
        "unstructured",
        "fastapi",
        "uvicorn",
    ],
    entry_points={
        "console_scripts": [
            "egp-ingest=tools.cli:main",
            "egp-chunk=tools.cli:main",
            "egp-graph=tools.cli:main",
            "egp-check=tools.cli:main",
            "egp-api=tools.cli:main",
        ]
    },
    python_requires=">=3.10",
)
