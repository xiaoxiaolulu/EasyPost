# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: executor.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x65xecutor.proto\"6\n\tInterface\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06method\x18\x03 \x01(\t\"<\n\nValidators\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x0e\n\x06\x61\x63tual\x18\x02 \x01(\t\x12\x0e\n\x06\x65xpect\x18\x03 \x01(\t\"\xa7\x01\n\x07Request\x12 \n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x12.Request.DataEntry\x12 \n\x04json\x18\x02 \x03(\x0b\x32\x12.Request.JsonEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a+\n\tJsonEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\":\n\x07\x45xtract\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"\xd1\x02\n\rApiDocRequest\x12\x0c\n\x04mode\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x1d\n\tinterface\x18\x03 \x01(\x0b\x32\n.Interface\x12,\n\x07headers\x18\x04 \x03(\x0b\x32\x1b.ApiDocRequest.HeadersEntry\x12\x19\n\x07request\x18\x05 \x01(\x0b\x32\x08.Request\x12\x14\n\x0csetup_script\x18\x06 \x01(\t\x12\x17\n\x0fteardown_script\x18\x07 \x01(\t\x12\x19\n\x07\x65xtract\x18\x08 \x03(\x0b\x32\x08.Extract\x12\x1f\n\nvalidators\x18\t \x03(\x0b\x32\x0b.Validators\x12 \n\x08\x63hildren\x18\n \x03(\x0b\x32\x0e.ApiDocRequest\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"u\n\x11ValidateExtractor\x12\x10\n\x08\x65xpected\x18\x01 \x01(\t\x12\x0f\n\x07methods\x18\x02 \x01(\t\x12\x0e\n\x06\x61\x63tual\x18\x03 \x01(\t\x12\x0e\n\x06result\x18\x04 \x01(\t\x12\r\n\x05state\x18\x05 \x01(\t\x12\x0e\n\x06\x65xpect\x18\x06 \x01(\t\"T\n\rDataExtractor\x12\x11\n\tvars_name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x12\n\nexpression\x18\x03 \x01(\t\x12\x0e\n\x06result\x18\x04 \x01(\t\"\xb1\x03\n\x05\x43\x61ses\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08log_data\x18\x02 \x03(\t\x12\r\n\x05l_env\x18\x03 \x03(\t\x12\r\n\x05g_env\x18\x04 \x03(\t\x12\x10\n\x08hook_gen\x18\x05 \x03(\t\x12\x0b\n\x03url\x18\x06 \x01(\t\x12\x0e\n\x06method\x18\x07 \x01(\t\x12\x13\n\x0bstatus_code\x18\x08 \x01(\x05\x12\x16\n\x0e\x63ontent_length\x18\t \x01(\x03\x12\x14\n\x0c\x63ontent_type\x18\n \x01(\t\x12\x17\n\x0fresponse_header\x18\x0b \x01(\t\x12\x17\n\x0frequests_header\x18\x0c \x01(\t\x12\x15\n\rresponse_body\x18\r \x01(\t\x12\x1a\n\x12performance_figure\x18\x0e \x01(\t\x12\r\n\x05\x63ount\x18\x0f \x01(\x05\x12\r\n\x05state\x18\x10 \x01(\t\x12\x0b\n\x03tag\x18\x11 \x01(\t\x12\x10\n\x08run_time\x18\x12 \x01(\t\x12.\n\x12validate_extractor\x18\x13 \x03(\x0b\x32\x12.ValidateExtractor\x12&\n\x0e\x64\x61ta_extractor\x18\x14 \x03(\x0b\x32\x0e.DataExtractor\"\x87\x01\n\tClassList\x12\x0b\n\x03\x61ll\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x05\x12\r\n\x05\x65rror\x18\x03 \x01(\x05\x12\x0c\n\x04\x66\x61il\x18\x04 \x01(\x05\x12\x15\n\x05\x63\x61ses\x18\x05 \x03(\x0b\x32\x06.Cases\x12\x0b\n\x03res\x18\x06 \x01(\t\x12\x0c\n\x04name\x18\x07 \x01(\t\x12\r\n\x05state\x18\x08 \x01(\t\"\xd3\x01\n\x0e\x41piDocResponse\x12\x0b\n\x03\x61ll\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x05\x12\r\n\x05\x65rror\x18\x03 \x01(\x05\x12\x0c\n\x04\x66\x61il\x18\x04 \x01(\x05\x12\x0f\n\x07runtime\x18\x05 \x01(\t\x12\x0f\n\x07\x61rgtime\x18\x06 \x01(\t\x12\x12\n\nbegin_time\x18\x07 \x01(\t\x12\x11\n\tpass_rate\x18\x08 \x01(\t\x12\r\n\x05state\x18\t \x01(\t\x12\x0e\n\x06tester\x18\n \x01(\t\x12\x1e\n\nclass_list\x18\x0b \x03(\x0b\x32\n.ClassList2?\n\x0f\x45xecutorService\x12,\n\tRunApiDoc\x12\x0e.ApiDocRequest\x1a\x0f.ApiDocResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'executor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REQUEST_DATAENTRY']._loaded_options = None
  _globals['_REQUEST_DATAENTRY']._serialized_options = b'8\001'
  _globals['_REQUEST_JSONENTRY']._loaded_options = None
  _globals['_REQUEST_JSONENTRY']._serialized_options = b'8\001'
  _globals['_APIDOCREQUEST_HEADERSENTRY']._loaded_options = None
  _globals['_APIDOCREQUEST_HEADERSENTRY']._serialized_options = b'8\001'
  _globals['_INTERFACE']._serialized_start=18
  _globals['_INTERFACE']._serialized_end=72
  _globals['_VALIDATORS']._serialized_start=74
  _globals['_VALIDATORS']._serialized_end=134
  _globals['_REQUEST']._serialized_start=137
  _globals['_REQUEST']._serialized_end=304
  _globals['_REQUEST_DATAENTRY']._serialized_start=216
  _globals['_REQUEST_DATAENTRY']._serialized_end=259
  _globals['_REQUEST_JSONENTRY']._serialized_start=261
  _globals['_REQUEST_JSONENTRY']._serialized_end=304
  _globals['_EXTRACT']._serialized_start=306
  _globals['_EXTRACT']._serialized_end=364
  _globals['_APIDOCREQUEST']._serialized_start=367
  _globals['_APIDOCREQUEST']._serialized_end=704
  _globals['_APIDOCREQUEST_HEADERSENTRY']._serialized_start=658
  _globals['_APIDOCREQUEST_HEADERSENTRY']._serialized_end=704
  _globals['_VALIDATEEXTRACTOR']._serialized_start=706
  _globals['_VALIDATEEXTRACTOR']._serialized_end=823
  _globals['_DATAEXTRACTOR']._serialized_start=825
  _globals['_DATAEXTRACTOR']._serialized_end=909
  _globals['_CASES']._serialized_start=912
  _globals['_CASES']._serialized_end=1345
  _globals['_CLASSLIST']._serialized_start=1348
  _globals['_CLASSLIST']._serialized_end=1483
  _globals['_APIDOCRESPONSE']._serialized_start=1486
  _globals['_APIDOCRESPONSE']._serialized_end=1697
  _globals['_EXECUTORSERVICE']._serialized_start=1699
  _globals['_EXECUTORSERVICE']._serialized_end=1762
# @@protoc_insertion_point(module_scope)
