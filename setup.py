import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

print(setuptools.find_packages('src', exclude=['main_window.py']))

setuptools.setup(
    name="extended-tabs",
    version="0.0.4",
    author="Ainur Giniyatov",
    # author_email="author@example.com",
    # description="A small example package",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/ainur-giniyatov/extended_tabs.git",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=['PyQt5'],
)
