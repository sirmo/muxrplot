.PHONY: test install pep8 release clean

test: pep8
    py.test --cov -l --tb=short --maxfail=1 program/

install:
		python setup.py develop

activate:
	. env/bin/activate

pep8:
	@flake8 program --ignore=F403 --exclude=junk

release: test
	@python setup.py sdist bdist_wheel upload

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
