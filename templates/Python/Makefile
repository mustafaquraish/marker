all: candidates

candidates: functions.py
	mkdir -p candidates/s1
	mkdir -p candidates/s2
	cp functions.py candidates/s1/
	cp functions.py candidates/s2/

.PHONY: clean all

clean:
	rm -rf marksheet.yml candidates