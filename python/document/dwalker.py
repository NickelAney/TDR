from hotpot.hotpot.hp_config import *
from hotpot.hotdata.syntactic_node import *
import sys
import os

class DWalker:
	def __init__(self, document, output_dir):
		self.document = document
		self.output_dir = output_dir
		self.enum_list = {}
#		os.makedirs(output_dir, 0o777, True)
		ofile_name = output_dir + '/' + document['file_name'].rstrip('.hd') + '.h'
		self.fout = open(ofile_name, "w")

	def __del__(self):
		self.fout.close()
		
	def get_symbol_access_by_type_suffix(self, identifier, type):
		if(type['type'] == E_SNT_CONTAINER):
			if(type['ct'] == E_CT_VECTOR):
				return '[i]'
		return ''

	def get_symbol_access_by_type_prefix(self, identifier, type, args):
		if(type['type'] == E_SNT_SIMPLE):
			return ''
		elif(type['type'] == E_SNT_CONTAINER):
			if(type['ct'] == E_CT_VECTOR):
				if(args['arg_list'][0]['type'] == E_SNT_SIMPLE):
					return ''
				else:
					return '&'
			elif(type['ct'] == E_CT_STRING):
				return ''
		elif(type['type'] == E_SNT_REFER):
			if(self.enum_list[type['ot']] == nil):
				return '&'
			else:
				return ''
		return ''

	def get_symbol_access_by_type_prefix_reverse(self, identifier, type, args):
		if(type['type'] == E_SNT_SIMPLE):
			return ''
		elif(type['type'] == E_SNT_CONTAINER):
			if(type['ct'] == E_CT_VECTOR):
				if(args['arg_list'][0]['type'] == E_SNT_SIMPLE):
					return ''
				else:
					return '*'
			elif(type['ct'] == E_CT_STRING):
				return ''
		elif(type['type'] == E_SNT_REFER):
			if(self['enum_list']['type']['ot'] == None):
				return '*'
			else:
				return ''
		return ''

	def get_symbol_access(self, identifier, obj):
		if(obj != None):
			for v in obj['parameters']['par_list']:
				if(v['identifier'] == identifier):
					prefix = self.get_symbol_access_by_type_prefix(identifier, v['type'], v['args'])
					suffix = self.get_symbol_access_by_type_suffix(identifier, v['type'], v['args'])
					return prefix + identifier + suffix

			for v in obj['field_list']['field_list']:
				if(v['identifier'] == identifier):
					prefix = self.get_symbol_access_by_type_prefix(identifier, v.type, v.args)
					suffix = self.get_symbol_access_by_type_suffix(identifier, v.type, v.args)
				return prefix + 'data->' + identifier + suffix

		return identifier

	def get_val(self, val, obj):
		if val['type'] == E_SNVT_IDENTIFIER :
			return self.get_symbol_access(val['val']['identifier'], obj)
		elif val['type'] == E_SNVT_CHAR:
			return val['val']['c']
		elif val['type'] == E_SNVT_DOUBLE:
			return val['val']['d']
		elif val['type'] == E_SNVT_BOOL:
			return val['val']['b']
		elif val['type'] == E_SNVT_STRING:
			return '"' + val['val']['str'] + '"'
		elif val['type'] == E_SNVT_INT64:
			return val['val']['i64']
		elif val['type'] == E_SNVT_UINT64:
			return val['val']['ui64']
		elif val['type'] == E_SNVT_HEX_INT64:
			return val['val']['hex_i64']
		elif val['type'] == E_SNVT_HEX_UINT64:
			return val['val']['hex_ui64']

	def get_type(self, type, args):
		if(type['type'] == E_SNT_SIMPLE):
			if(type['st'] == E_ST_CHAR):
				return 'hpchar'
			elif(type['st'] == E_ST_DOUBLE):
				return 'hpdouble'
			elif(type['st'] == E_ST_BOOL):
				return 'hpbool'
			elif(type['st'] == E_ST_INT8):
				return 'hpint8'
			elif(type['st'] == E_ST_INT16):
				return 'hpint16'
			elif(type['st'] == E_ST_INT32):
				return 'hpint32'
			elif(type['st'] == E_ST_INT64):
				return 'hpint64'
			elif(type['st'] == E_ST_UINT8):
				return 'hpuint8'
			elif(type['st'] == E_ST_UINT16):
				return 'hpuint16'
			elif(type['st'] == E_ST_UINT32):
				return 'hpuint32'
			elif(type['st'] == E_ST_UINT64):
				return 'hpuint64'
		elif(type['type'] == E_SNT_CONTAINER):
			if(type['ct'] == E_CT_VECTOR):
				return args['arg_list'][0]['ot']
			elif(type['ct'] == E_CT_STRING):
				return 'hpchar'
		elif(type['type'] == E_SNT_REFER):
			return type['ot'];

	def print_file_prefix(self):
		self.print_line(0, '/**')
		self.print_line(0, ' * Autogenerated by HotData (' + HOTPOT_VERSION + ')')
		self.print_line(0, ' *')
		self.print_line(0, ' * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING')
		self.print_line(0, ' *  @generated')
		self.print_line(0, ' */')
		self.print_line(0, '')

	def print_line(self, n, str):
		for i in range(0,n):
			self.fout.write('    ')
		self.fout.write(str)
		self.fout.write('\n')

	def on_document_begin(self, document):
		pass

	def on_document_end(self, document):
		pass

	def on_const(self, const):
		pass

	def on_typedef(self, typedef):
		pass

	def on_enum_field(self, enum_field):
		pass

	def on_enum_begin(self, enum):
		pass

	def on_enum_end(self, enum):
		pass

	def on_enum(self, enum):
		self.on_enum_begin(enum)
		for enum_field in enum['enum_def_list']:
			self.on_enum_field(enum_field)
		self.on_enum_end(enum)

	def on_struct_field(self, struct_field):
		pass

	def on_struct_begin(self, struct):
		pass

	def on_struct_end(self, struct):
		pass

	def on_struct(self, struct):
		self.on_struct_begin(struct)
		for struct_field in struct['field_list']['field_list']:
			self.on_struct_field(struct_field)
		self.on_struct_end(struct)

	def on_union_field(self, union_field):
		pass

	def on_union_begin(self, union):
		pass

	def on_union_end(self, union):
		pass

	def on_union(self, union):
		self.on_union_begin(union)
		for union_field in union['field_list']['field_list']:
			self.on_union_field(union_field)
		self.on_union_end(union)

	def on_import(self, de_import):
		pass

	def on_unix_comment(self, de_unix_comment):
		pass

	def walk(self):
		self.on_document_begin(self.document)
		for definition in self.document['definition_list']:
			if(definition['type'] == E_DT_CONST):
				self.on_const(definition['definition']['de_const'])
			elif(definition['type'] == E_DT_TYPEDEF):
				self.on_typedef(definition['definition']['de_typedef'])
			elif(definition['type'] == E_DT_ENUM):
				self.on_enum(definition['definition']['de_enum'])
			elif(definition['type'] == E_DT_STRUCT):
				self.on_struct(definition['definition']['de_struct'])
			elif(definition['type'] == E_DT_UNION):
				self.on_union(definition['definition']['de_union'])
			elif(definition['type'] == E_DT_IMPORT):
				self.on_import(definition['definition']['de_import'])
			elif(definition['type'] == E_DT_UNIX_COMMENT):
				self.on_unix_comment(definition['definition']['de_unix_comment'])
		self.on_document_end(self.document)
