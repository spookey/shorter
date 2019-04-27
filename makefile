DEBUG		:=	1
ENVIRON		:=	development
FLASK		:=	application.py

_HOST		:=	::1
_PORT		:=	5000

CMD_VENV	:=	virtualenv
DIR_VENV	:=	venv
VER_PY		:=	3.7
CMD_PIP		:=	$(DIR_VENV)/bin/pip$(VER_PY)
CMD_PY		:=	$(DIR_VENV)/bin/python$(VER_PY)
CMD_PYTEST	:=	$(DIR_VENV)/bin/pytest
CMD_PYREV	:=	$(DIR_VENV)/bin/pyreverse
CMD_PYLINT	:=	$(DIR_VENV)/bin/pylint
CMD_ISORT	:=	$(DIR_VENV)/bin/isort
CMD_FLASK	:=	$(DIR_VENV)/bin/flask

DIR_SHORTER	:=	shorter
DIR_TESTS	:=	tests
DIR_LOGS	:=	logs

.PHONY: help
help:
	@echo "make shorter"
	@echo "————————————"
	@echo
	@echo "venv             install virtualenv"
	@echo "reqs             install requirements into venv"
	@echo
	@echo "lint             run pylint"
	@echo "plot             run pyreverse"
	@echo "sort             run isort"
	@echo "test             run pytest"
	@echo "tcov, tcovh      run test coverage (html)"
	@echo
	@echo "clean            show files to clean"
	@echo "cleanup          clean files unknown to git"
	@echo
	@echo "run              run application"
	@echo "shell            launch a shell"
	@echo
	@echo "                 🦑"
	@echo


###
# plumbing

$(DIR_VENV):
	$(CMD_VENV) -p "python$(VER_PY)" "$(DIR_VENV)"

.PHONY: reqs reqs-dev
reqs: $(CMD_FLASK)
reqs-dev: $(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST)

$(CMD_FLASK): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements.txt"
$(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-dev.txt"


###
# service

define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

define _lint
	$(CMD_PYLINT) \
		--disable "C0111" \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			$(1)
endef

.PHONY: lint lintt
lint: $(CMD_PYLINT)
	$(call _lint,"$(DIR_SHORTER)")
lintt: $(CMD_PYLINT)
	$(call _lint,"$(DIR_TESTS)")


define _reverse
	$(CMD_PYREV) \
		--all-ancestors \
		--filter-mode="ALL" \
		--module-names="yes" \
		--output png \
		--project="$(1)$(2)" \
			$(1)
endef

.PHONY: plot plott
plot: $(CMD_PYREV)
	$(call _reverse,$(DIR_SHORTER))
plott: $(CMD_PYREV)
	$(call _reverse,$(DIR_TESTS),_$(DIR_SHORTER))


define _sort
	$(CMD_ISORT) -cs -fss -m=5 -y -rc $(1)
endef

.PHONY: sort sortt
sort: $(CMD_ISORT)
	$(call _sort,"$(DIR_SHORTER)")
sortt: $(CMD_ISORT)
	$(call _sort,"$(DIR_TESTS)")


define _test
	$(CMD_PYTEST) $(1) "$(DIR_TESTS)" -vv
endef
define _tcov
	$(call _test,$(1) --cov="$(DIR_SHORTER)")
endef

.PHONY: test tcov tcovh
test: $(CMD_PYTEST)
	$(call _test,)
tcov: $(CMD_PYTEST)
	$(call _tcov,)
tcovh: $(CMD_PYTEST)
	$(call _tcov,--cov-report="html")

###
# cleanup

define _gitclean
	git clean \
		-e "*.py" \
		-e "$(DIR_LOGS)/" \
		-e "$(DIR_VENV)/" \
		$(1)
endef

.PHONY: clean cleanup
clean:
	$(call _gitclean,-ndx)
cleanup:
	$(call _gitclean,-fdx)


###
# flask

define _flask
	FLASK_DEBUG="$(DEBUG)" \
	FLASK_ENV="$(ENVIRON)" \
	FLASK_APP="$(FLASK)" \
	$(CMD_FLASK) $(1)
endef

.PHONY: shell run
run: $(CMD_FLASK)
	$(call _flask,run --host "$(_HOST)" --port "$(_PORT)")
shell: $(CMD_FLASK)
	$(call _flask,shell)
