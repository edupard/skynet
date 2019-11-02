# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0emessages.proto\"\x9f\x01\n\tStockData\x12\t\n\x01o\x18\x01 \x01(\x01\x12\t\n\x01h\x18\x02 \x01(\x01\x12\t\n\x01l\x18\x03 \x01(\x01\x12\t\n\x01\x63\x18\x04 \x01(\x01\x12\t\n\x01v\x18\x05 \x01(\x01\x12\x0b\n\x03\x61_o\x18\x06 \x01(\x01\x12\x0b\n\x03\x61_h\x18\x07 \x01(\x01\x12\x0b\n\x03\x61_l\x18\x08 \x01(\x01\x12\x0b\n\x03\x61_c\x18\t \x01(\x01\x12\x0b\n\x03\x61_v\x18\n \x01(\x01\x12\x0b\n\x03\x64iv\x18\x0b \x01(\x01\x12\r\n\x05split\x18\x0c \x01(\x01\"v\n\tDailyData\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\x05\x12\"\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x14.DailyData.DataEntry\x1a\x37\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x19\n\x05value\x18\x02 \x01(\x0b\x32\n.StockData:\x02\x38\x01\"\x92\x01\n\x05\x43hunk\x12\x0c\n\x04year\x18\x01 \x01(\x05\x12\r\n\x05month\x18\x02 \x01(\x05\x12,\n\x0b\x64\x61ilyChunks\x18\x03 \x03(\x0b\x32\x17.Chunk.DailyChunksEntry\x1a>\n\x10\x44\x61ilyChunksEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x19\n\x05value\x18\x02 \x01(\x0b\x32\n.DailyData:\x02\x38\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_STOCKDATA = _descriptor.Descriptor(
  name='StockData',
  full_name='StockData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='o', full_name='StockData.o', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='h', full_name='StockData.h', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='l', full_name='StockData.l', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='c', full_name='StockData.c', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='v', full_name='StockData.v', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='a_o', full_name='StockData.a_o', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='a_h', full_name='StockData.a_h', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='a_l', full_name='StockData.a_l', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='a_c', full_name='StockData.a_c', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='a_v', full_name='StockData.a_v', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='div', full_name='StockData.div', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='split', full_name='StockData.split', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=178,
)


_DAILYDATA_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='DailyData.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='DailyData.DataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='DailyData.DataEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=243,
  serialized_end=298,
)

_DAILYDATA = _descriptor.Descriptor(
  name='DailyData',
  full_name='DailyData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='DailyData.date', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='DailyData.data', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DAILYDATA_DATAENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=298,
)


_CHUNK_DAILYCHUNKSENTRY = _descriptor.Descriptor(
  name='DailyChunksEntry',
  full_name='Chunk.DailyChunksEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Chunk.DailyChunksEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='Chunk.DailyChunksEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=385,
  serialized_end=447,
)

_CHUNK = _descriptor.Descriptor(
  name='Chunk',
  full_name='Chunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='year', full_name='Chunk.year', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='month', full_name='Chunk.month', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dailyChunks', full_name='Chunk.dailyChunks', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CHUNK_DAILYCHUNKSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=447,
)

_DAILYDATA_DATAENTRY.fields_by_name['value'].message_type = _STOCKDATA
_DAILYDATA_DATAENTRY.containing_type = _DAILYDATA
_DAILYDATA.fields_by_name['data'].message_type = _DAILYDATA_DATAENTRY
_CHUNK_DAILYCHUNKSENTRY.fields_by_name['value'].message_type = _DAILYDATA
_CHUNK_DAILYCHUNKSENTRY.containing_type = _CHUNK
_CHUNK.fields_by_name['dailyChunks'].message_type = _CHUNK_DAILYCHUNKSENTRY
DESCRIPTOR.message_types_by_name['StockData'] = _STOCKDATA
DESCRIPTOR.message_types_by_name['DailyData'] = _DAILYDATA
DESCRIPTOR.message_types_by_name['Chunk'] = _CHUNK

StockData = _reflection.GeneratedProtocolMessageType('StockData', (_message.Message,), dict(
  DESCRIPTOR = _STOCKDATA,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:StockData)
  ))
_sym_db.RegisterMessage(StockData)

DailyData = _reflection.GeneratedProtocolMessageType('DailyData', (_message.Message,), dict(

  DataEntry = _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), dict(
    DESCRIPTOR = _DAILYDATA_DATAENTRY,
    __module__ = 'messages_pb2'
    # @@protoc_insertion_point(class_scope:DailyData.DataEntry)
    ))
  ,
  DESCRIPTOR = _DAILYDATA,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:DailyData)
  ))
_sym_db.RegisterMessage(DailyData)
_sym_db.RegisterMessage(DailyData.DataEntry)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), dict(

  DailyChunksEntry = _reflection.GeneratedProtocolMessageType('DailyChunksEntry', (_message.Message,), dict(
    DESCRIPTOR = _CHUNK_DAILYCHUNKSENTRY,
    __module__ = 'messages_pb2'
    # @@protoc_insertion_point(class_scope:Chunk.DailyChunksEntry)
    ))
  ,
  DESCRIPTOR = _CHUNK,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:Chunk)
  ))
_sym_db.RegisterMessage(Chunk)
_sym_db.RegisterMessage(Chunk.DailyChunksEntry)


_DAILYDATA_DATAENTRY.has_options = True
_DAILYDATA_DATAENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
_CHUNK_DAILYCHUNKSENTRY.has_options = True
_CHUNK_DAILYCHUNKSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
