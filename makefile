test:
	python3 -Bm unittest

check: # dependency check
	which node
	which bun
	which gum
	which python3


.PHONY: test check