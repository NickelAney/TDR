#include "generate/tlibc_writer_header.h"
#include "generate/tlibc_types.h"
#include "symbols.h"
#include "generator.h"
#include "version.h"

#include <stdio.h>
#include <string.h>

static TD_ERROR_CODE on_document_begin(GENERATOR *super, const char *file_name)
{
	char types_header[MAX_PACKAGE_NAME_LENGTH];	

	generator_open(super, file_name, TLIBC_WRITER_HEADER_SUFFIX);

	generator_print(super, "/**\n");
    generator_print(super, " * Autogenerated by TData Compiler (%s)\n", TDATA_VERSION);
    generator_print(super, " *\n");
    generator_print(super, " * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING\n");
    generator_print(super, " *  @generated\n");
    generator_print(super, " */\n");
	generator_print(super, "\n");



	generator_print(super, "#ifndef _H_%s\n", super->document_name);
	generator_print(super, "#define _H_%s\n", super->document_name);
	generator_print(super, "\n");
	generator_print(super, "#include \"platform/tlibc_platform.h\"\n");
	generator_print(super, "#include \"protocol/tlibc_abstract_writer.h\"\n");
	generator_print(super, "#include \"core/tlibc_error_code.h\"\n");
	generator_print(super, "#include \"tdata/tdata_types.h\"\n");
	
	//包含types的头文件
	strncpy(types_header, file_name, MAX_PACKAGE_NAME_LENGTH);
	types_header[MAX_PACKAGE_NAME_LENGTH - 1] = 0;
	generator_replace_extension(types_header, MAX_PACKAGE_NAME_LENGTH, TLIBC_TYPES_SUFFIX);
	generator_print(super, "#include \"%s\"\n", types_header);
	
	generator_print(super, "\n");
	generator_print(super, "\n");
	return E_TD_NOERROR;
}

static TD_ERROR_CODE on_document_end(GENERATOR *super, const char *file_name)
{
	TLIBC_UNUSED(file_name);

	generator_print(super, "\n");
	generator_print(super, "#endif //_H_%s\n", super->document_name);
	generator_print(super, "\n");

	generator_close(super);
	return E_TD_NOERROR;
}

static TD_ERROR_CODE _on_import(TLIBC_WRITER_HEADER_GENERATOR *self, const ST_Import *de_import)
{
	char name[MAX_PACKAGE_NAME_LENGTH];	
	strncpy(name, de_import->package_name, MAX_PACKAGE_NAME_LENGTH);
	name[MAX_PACKAGE_NAME_LENGTH - 1] = 0;
	generator_replace_extension(name, MAX_PACKAGE_NAME_LENGTH, TLIBC_WRITER_HEADER_SUFFIX);
	generator_print(&self->super, "#include \"%s\"\n", name);

	return E_TD_NOERROR;
}



static TD_ERROR_CODE _on_enum(TLIBC_WRITER_HEADER_GENERATOR *self, const ST_ENUM *de_enum)
{
	generator_print(&self->super, "\n");

	generator_print(&self->super, "TLIBC_ERROR_CODE tlibc_write_%s(TLIBC_ABSTRACT_WRITER *self, const %s *data);\n", de_enum->name, de_enum->name);

	return E_TD_NOERROR;
}

static TD_ERROR_CODE _on_struct(TLIBC_WRITER_HEADER_GENERATOR *self, const ST_STRUCT *de_struct)
{
	generator_print(&self->super, "\n");

	generator_print(&self->super, "TLIBC_ERROR_CODE tlibc_write_%s(TLIBC_ABSTRACT_WRITER *self, const %s *data);\n", de_struct->name, de_struct->name);

	return E_TD_NOERROR;
}

static TD_ERROR_CODE _on_union(TLIBC_WRITER_HEADER_GENERATOR *self, const ST_UNION *de_union)
{
	generator_print(&self->super, "\n");

	generator_print(&self->super, "TLIBC_ERROR_CODE tlibc_write_%s(TLIBC_ABSTRACT_WRITER *self, const %s *data, %s selector);\n", de_union->name, de_union->name, de_union->parameters.par_list[0].type.st_refer);
	return E_TD_NOERROR;
}

static TD_ERROR_CODE on_definition(GENERATOR *super, const ST_DEFINITION *definition)
{
	TLIBC_WRITER_HEADER_GENERATOR *self = TLIBC_CONTAINER_OF(super, TLIBC_WRITER_HEADER_GENERATOR, super);
	switch(definition->type)
	{
		case E_DT_IMPORT:
			return _on_import(self, &definition->definition.de_import);				
		case E_DT_CONST:
			return E_TD_NOERROR;
		case E_DT_ENUM:
			return _on_enum(self, &definition->definition.de_enum);
		case E_DT_STRUCT:
			return _on_struct(self, &definition->definition.de_struct);
		case E_DT_UNION:
			return _on_union(self, &definition->definition.de_union);
		case E_DT_TYPEDEF:
			return E_TD_NOERROR;
		case E_DT_UNIX_COMMENT:
			return E_TD_NOERROR;
		default:
			return E_TD_ERROR;
	}
}

void tlibc_writer_header_generator_init(TLIBC_WRITER_HEADER_GENERATOR *self, const SYMBOLS *symbols)
{
	generator_init(&self->super, symbols);

	self->super.on_document_begin = on_document_begin;
	self->super.on_document_end = on_document_end;
	self->super.on_definition = on_definition;
}
