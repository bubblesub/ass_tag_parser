release:
	rm -rf dist
	python3 setup.py sdist
	twine upload dist/*

test:
	pytest --cov=ass_tag_parser --cov-report term-missing

lint:
	pre-commit run -a

clean:
	rm .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache

.PHONY: release test lint clean
