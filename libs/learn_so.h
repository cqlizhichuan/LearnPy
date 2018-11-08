#ifndef __LEARN_SO_H__
#define __LEARN_SO_H__

#ifndef SUCCESS
#define SUCCESS (0)
#endif

#ifndef FAIL
#define FAIL (-1)
#endif

typedef struct
{
	char *name;
	int age;
}person_t;

typedef struct tag_node
{
	person_t p;
	struct tag_node *next;
}node_t;

typedef struct tag_list
{
	node_t *head;
	node_t *tail;
}list_s;

int max(int x, int y);
int add_new_person(person_t *new_person);
int init_person_list();
void free_person_list();
int create_fake_persons();

#endif