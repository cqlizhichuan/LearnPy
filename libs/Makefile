.PHONY: build test clean

build: liblearn_so.so

liblearn_so.so: learn_so.o
	gcc -o $@ -shared $<

learn_so.o:learn_so.c
	gcc -c -fPIC $<

test: a.out

a.out: test.c liblearn_so.so
	gcc test.c -L . -l learn_so
	LD_LIBRARY_PATH=. ./a.out

clean:
	rm -f *.o *.so *.out
