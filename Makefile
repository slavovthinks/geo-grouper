start:
	export PYTHONPATH=$$PWD; uvicorn geo_grouper.app:app --reload

test:
	pytest --cov=geo_grouoer tests/
