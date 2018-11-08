#include <stdio.h>
#include "learn_so.h"

int main(int argc, char **argv)
{
	person_t p;
	p.name = "wuaihong";
	p.age = 26;
	add_new_person(&p);
	return 0;
}