# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dir_struct.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='dir_struct.proto',
  package='tg_sticker_to_wechat',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x10\x64ir_struct.proto\x12\x14tg_sticker_to_wechat\"x\n\x07Sticker\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\t\x12\x0e\n\x06\x64oc_id\x18\x02 \x01(\x03\x12\x10\n\x08\x65moticon\x18\x03 \x01(\t\x12\x11\n\textension\x18\x04 \x01(\t\x12\x15\n\roriginal_size\x18\x05 \x01(\x03\x12\x10\n\x08gif_size\x18\x06 \x01(\x03\"\xf2\x01\n\nStickerSet\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0c\n\x04hash\x18\x02 \x01(\x05\x12\x12\n\nshort_name\x18\x03 \x01(\t\x12\r\n\x05title\x18\x04 \x01(\t\x12>\n\x07sticker\x18\x05 \x03(\x0b\x32-.tg_sticker_to_wechat.StickerSet.StickerEntry\x12\x18\n\x10update_timestamp\x18\x06 \x01(\x01\x1aM\n\x0cStickerEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.tg_sticker_to_wechat.Sticker:\x02\x38\x01\"\xb4\x01\n\tDirStruct\x12\x44\n\x0bsticker_set\x18\x01 \x03(\x0b\x32/.tg_sticker_to_wechat.DirStruct.StickerSetEntry\x12\x0c\n\x04hash\x18\x02 \x01(\x03\x1aS\n\x0fStickerSetEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12/\n\x05value\x18\x02 \x01(\x0b\x32 .tg_sticker_to_wechat.StickerSet:\x02\x38\x01')
)




_STICKER = _descriptor.Descriptor(
  name='Sticker',
  full_name='tg_sticker_to_wechat.Sticker',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_id', full_name='tg_sticker_to_wechat.Sticker.file_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='doc_id', full_name='tg_sticker_to_wechat.Sticker.doc_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='emoticon', full_name='tg_sticker_to_wechat.Sticker.emoticon', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extension', full_name='tg_sticker_to_wechat.Sticker.extension', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='original_size', full_name='tg_sticker_to_wechat.Sticker.original_size', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gif_size', full_name='tg_sticker_to_wechat.Sticker.gif_size', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=162,
)


_STICKERSET_STICKERENTRY = _descriptor.Descriptor(
  name='StickerEntry',
  full_name='tg_sticker_to_wechat.StickerSet.StickerEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tg_sticker_to_wechat.StickerSet.StickerEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tg_sticker_to_wechat.StickerSet.StickerEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=407,
)

_STICKERSET = _descriptor.Descriptor(
  name='StickerSet',
  full_name='tg_sticker_to_wechat.StickerSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='tg_sticker_to_wechat.StickerSet.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='tg_sticker_to_wechat.StickerSet.hash', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='short_name', full_name='tg_sticker_to_wechat.StickerSet.short_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='title', full_name='tg_sticker_to_wechat.StickerSet.title', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sticker', full_name='tg_sticker_to_wechat.StickerSet.sticker', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_timestamp', full_name='tg_sticker_to_wechat.StickerSet.update_timestamp', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_STICKERSET_STICKERENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=165,
  serialized_end=407,
)


_DIRSTRUCT_STICKERSETENTRY = _descriptor.Descriptor(
  name='StickerSetEntry',
  full_name='tg_sticker_to_wechat.DirStruct.StickerSetEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tg_sticker_to_wechat.DirStruct.StickerSetEntry.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tg_sticker_to_wechat.DirStruct.StickerSetEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=507,
  serialized_end=590,
)

_DIRSTRUCT = _descriptor.Descriptor(
  name='DirStruct',
  full_name='tg_sticker_to_wechat.DirStruct',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sticker_set', full_name='tg_sticker_to_wechat.DirStruct.sticker_set', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='tg_sticker_to_wechat.DirStruct.hash', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DIRSTRUCT_STICKERSETENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=410,
  serialized_end=590,
)

_STICKERSET_STICKERENTRY.fields_by_name['value'].message_type = _STICKER
_STICKERSET_STICKERENTRY.containing_type = _STICKERSET
_STICKERSET.fields_by_name['sticker'].message_type = _STICKERSET_STICKERENTRY
_DIRSTRUCT_STICKERSETENTRY.fields_by_name['value'].message_type = _STICKERSET
_DIRSTRUCT_STICKERSETENTRY.containing_type = _DIRSTRUCT
_DIRSTRUCT.fields_by_name['sticker_set'].message_type = _DIRSTRUCT_STICKERSETENTRY
DESCRIPTOR.message_types_by_name['Sticker'] = _STICKER
DESCRIPTOR.message_types_by_name['StickerSet'] = _STICKERSET
DESCRIPTOR.message_types_by_name['DirStruct'] = _DIRSTRUCT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Sticker = _reflection.GeneratedProtocolMessageType('Sticker', (_message.Message,), {
  'DESCRIPTOR' : _STICKER,
  '__module__' : 'dir_struct_pb2'
  # @@protoc_insertion_point(class_scope:tg_sticker_to_wechat.Sticker)
  })
_sym_db.RegisterMessage(Sticker)

StickerSet = _reflection.GeneratedProtocolMessageType('StickerSet', (_message.Message,), {

  'StickerEntry' : _reflection.GeneratedProtocolMessageType('StickerEntry', (_message.Message,), {
    'DESCRIPTOR' : _STICKERSET_STICKERENTRY,
    '__module__' : 'dir_struct_pb2'
    # @@protoc_insertion_point(class_scope:tg_sticker_to_wechat.StickerSet.StickerEntry)
    })
  ,
  'DESCRIPTOR' : _STICKERSET,
  '__module__' : 'dir_struct_pb2'
  # @@protoc_insertion_point(class_scope:tg_sticker_to_wechat.StickerSet)
  })
_sym_db.RegisterMessage(StickerSet)
_sym_db.RegisterMessage(StickerSet.StickerEntry)

DirStruct = _reflection.GeneratedProtocolMessageType('DirStruct', (_message.Message,), {

  'StickerSetEntry' : _reflection.GeneratedProtocolMessageType('StickerSetEntry', (_message.Message,), {
    'DESCRIPTOR' : _DIRSTRUCT_STICKERSETENTRY,
    '__module__' : 'dir_struct_pb2'
    # @@protoc_insertion_point(class_scope:tg_sticker_to_wechat.DirStruct.StickerSetEntry)
    })
  ,
  'DESCRIPTOR' : _DIRSTRUCT,
  '__module__' : 'dir_struct_pb2'
  # @@protoc_insertion_point(class_scope:tg_sticker_to_wechat.DirStruct)
  })
_sym_db.RegisterMessage(DirStruct)
_sym_db.RegisterMessage(DirStruct.StickerSetEntry)


_STICKERSET_STICKERENTRY._options = None
_DIRSTRUCT_STICKERSETENTRY._options = None
# @@protoc_insertion_point(module_scope)