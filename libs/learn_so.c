#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "learn_so.h"

static node_t *person_list = NULL;
static FILE *fp = NULL;
static char *PERSON_RECORD = "person_list";

int max(int x, int y)
{
	return (x > y) ? x : y;
}

int add_person_info_to_file(char *filename, node_t *node)
{
	if (NULL == (fp = fopen(filename, "w")))
	{
		return FAIL;
	}

	person_t *p = &(node->p);
	//fprintf(fp, "%s,%d", "lizhichuan", 26);
	fprintf(fp, "%s,%d", p->name, p->age);
	fclose(fp);
	return SUCCESS;
}

int init_person_list()
{
	node_t *node = (node_t *)malloc(sizeof(node_t));
	if (node)
	{
		memset(node, 0, sizeof(node_t))	;
		person_list = node;
		return SUCCESS;
	}

	return FAIL;
}

int add_new_person(person_t *new_person)
{
	node_t *node = NULL;

	if (NULL == new_person)
	{
		return FAIL;
	}

	node = (node_t *)malloc(sizeof(node_t));
	if (node)
	{
		node->p.name = new_person->name;
		node->p.age = new_person->age;
		//memcpy(&(node->p), new_person, sizeof(person_t));
		add_person_info_to_file(PERSON_RECORD, node);
		return SUCCESS;
	}

	return FAIL;
}

void free_person_list()
{
	node_t *q = NULL;
	node_t *p = person_list;
	person_list = NULL;
	while(p)
	{
		q = p;
		p = p->next;
		if (q)
		{
			free(q);
		}
	}
}

int create_fake_persons()
{
	if (NULL == person_list)
	{
		return FAIL;
	}

	
	return SUCCESS;
}