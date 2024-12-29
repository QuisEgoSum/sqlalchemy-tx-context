from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='sqlalchemy_tx_context',
    version='0.4.2',
    author='QuisEgoSum',
    author_email='subbotin.evdokim@gmail.com',
    description='An extension for sqlalchemy',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/QuisEgoSum/sqlalchemy-tx-context',
    packages=find_packages(exclude=['tmp', 'example']),
    install_requires=[
        'SQLAlchemy>=2.0.0',
        'asyncpg>=0.29.0',
        'contextvars>=2.4'
    ],
    keywords='sqlalchemy',
    python_requires='>=3.7',
    license='MIT',
    include_package_data=True,
    package_data={
        'sqlalchemy_tx_context': ['*.pyi']
    }
)
