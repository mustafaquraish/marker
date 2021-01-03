all: candidates

candidates: functions.c
	mkdir -p candidates/s1
	mkdir -p candidates/s2
	cp functions.c candidates/s1/
	cp functions.c candidates/s2/

.PHONY: clean all

clean:
	rm -rf marksheet.yml candidates