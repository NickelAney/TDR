#ifndef _H_SCRIPT_PARSER
#define _H_SCRIPT_PARSER

#include <stdarg.h>
#include <stdio.h>

#include "hotpot/hp_platform.h"

#include "script_y.h"
#include "script_l.h"

#define MAX_INCLUDE_FILE_LEVEL 1024
typedef struct tagSCRIPT_PARSER_STACK_NODE
{
	FILE *f;
	YY_BUFFER_STATE bs;
}SCRIPT_PARSER_STACK_NODE;
typedef struct tagSCRIPT_PARSER SCRIPT_PARSER;
struct tagSCRIPT_PARSER
{
	yyscan_t scanner;
	hpint32 result;

	hpuint32 stack_num;
	SCRIPT_PARSER_STACK_NODE stack[MAX_INCLUDE_FILE_LEVEL];
};

hpint32 script_parser(SCRIPT_PARSER *self, const char* file_name);

hpint32 script_open_file(yyscan_t *super, const char *file_name);

hpint32 script_close_file(yyscan_t *super);

#endif//_H_SCRIPT_PARSER

