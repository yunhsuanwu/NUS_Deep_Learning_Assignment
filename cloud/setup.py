from setuptools import setup, find_packages

setup(
    name="cloud",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': {
            'web_scrapping = scripts.web_scrapping:main',
            'generate_real_clouds_dataset = scripts.generate_real_clouds_dataset:main',
            'generate_synthetic_clouds_dataset = scripts.generate_synthetic_clouds_dataset:main',
            'dataset_formatting = scripts.dataset_formatting:main',
        }
    },
)
