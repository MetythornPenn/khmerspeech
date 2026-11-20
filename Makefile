build:
	rm -rf *.egg-info/ dist/ khmerspeech/__pycache__
	python setup.py sdist

upload:
	twine upload dist/*
