.PHONY: all requirements tests

all: requirements

run:
	export FLASK_APP=run; export FLASK_ENV=development; flask run;

shell:
	export FLASK_APP=run; export FLASK_ENV=development; flask shell;

clean:
	@echo
	@echo "---- Clean *.pyc ----"
	@find . -name \*.pyc -delete

clean_pip: clean
	@echo
	@echo "---- Clean packages ----"
	@pip freeze | grep -v "^-e" | cut -d "@" -f1 | xargs pip uninstall -y

cleaninstall: requirements clean_pip
	@echo
	@echo "---- Install packages from requirements.txt ----"
	@pip install -r requirements.txt
	@echo
	@pip freeze
	@echo
	@echo "---- Install packages from setup ----"
	@$(shell echo ${PYTHON_ROCKSDB_FLAGS}) pip install -e ./

tests:
	pytest --cov=app --cov-config=.coveragerc --cov-report=html:htmlcov --cov-report xml:cov.xml --cov-report=term \
		-vv --doctest-modules --ignore-glob=./app/main.py --log-level=DEBUG --junitxml=report.xml ./app ./tests


testsx:
	pytest -x -vv --doctest-modules --ignore-glob=./identity_server/main.py --log-level=DEBUG ./identity_server ./tests
