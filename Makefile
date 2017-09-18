upload_to_pypi:
	pip install twine setuptools
	rm -rf dist/*
	rm -rf build/*
	python setup.py sdist build
	twine upload dist/*

test:
	nosetests -v