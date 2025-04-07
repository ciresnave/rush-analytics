# Build and Test Wheel Distribution

# Step 1: Build the wheel
python3 -m pip install --upgrade build
python3 -m build

# Step 2: Test the wheel on Test PyPI
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*

# Step 3: Verify installation from Test PyPI
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps rush-analytics