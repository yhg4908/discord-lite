# setup.py
from setuptools import setup, find_packages

setup(
    name="discord-lite",  # 패키지 이름
    version="0.1.0",  # 초기 버전
    description="A lightweight Discord API wrapper",  # 간단한 설명
    long_description=open("README.md").read(),  # 자세한 설명 (README.md에서 읽어옴)
    long_description_content_type="text/markdown",  # README 포맷
    url="https://github.com/yourusername/discord-lite",  # 프로젝트 URL
    author="Your Name",  # 작성자
    author_email="your.email@example.com",  # 작성자 이메일
    license="MIT",  # 라이센스
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="discord api lightweight bot",  # 키워드
    packages=find_packages(),  # 포함할 패키지
    install_requires=[
        "aiohttp>=3.8.0"  # 의존성 패키지
    ],
    python_requires=">=3.7",  # 필요한 Python 버전
    project_urls={  # 추가 링크
        "Bug Reports": "https://github.com/yourusername/discord-lite/issues",
        "Source": "https://github.com/yourusername/discord-lite",
    },
)
