pip uninstall -y extended_tabs
python setup.py clean --all
python setup.py bdist_wheel
pip install dist\extended_tabs-0.0.3-py3-none-any.whl
