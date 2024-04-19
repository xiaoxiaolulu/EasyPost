import os
import pathlib
from google.protobuf import descriptor_pb2 as desc_pb2
from google.protobuf import text_format


def parse_proto_and_generate_interface(proto_file_path, interface_dir_path):
    # 加载 Proto 文件
    with open(proto_file_path, 'rb') as f:
        file_descriptor_set = desc_pb2.FileDescriptorSet()
        file_descriptor_set.ParseFromString(f.read())

    # 创建接口目录
    if not os.path.exists(interface_dir_path):
        os.makedirs(interface_dir_path)

    # 处理每个消息类型
    for file_descriptor_proto in file_descriptor_set.file:
        for message_type_proto in file_descriptor_proto.message_type:
            message_type_name = message_type_proto.name
            interface_file_path = os.path.join(interface_dir_path, f'{message_type_name}.py')

            # 生成接口文件内容
            interface_file_content = generate_interface_file_content(message_type_proto)

            # 写入接口文件内容
            with open(interface_file_path, 'w') as f:
                f.write(interface_file_content)


def generate_interface_file_content(message_type_proto):
    # 提取消息类型名称和字段
    message_type_name = message_type_proto.name
    fields = message_type_proto.field

    # 生成接口文件内容
    interface_file_content = (
        f"""
        class {message_type_name}InputParameters:
            """
    )

    for field in fields:
        field_name = field.name
        field_type = field.type
        field_label = field.label

        # 根据类型和标签定义输入参数
        if field_type == desc_pb2.FieldDescriptorProto.TYPE_INT32:
            if field_label == desc_pb2.FieldDescriptorProto.LABEL_OPTIONAL:
                parameter_definition = f"            {field_name}: int = None"
            else:
                parameter_definition = f"            {field_name}: int"
        elif field_type == desc_pb2.FieldDescriptorProto.TYPE_STRING:
            if field_label == desc_pb2.FieldDescriptorProto.LABEL_OPTIONAL:
                parameter_definition = f"            {field_name}: str = None"
            else:
                parameter_definition = f"            {field_name}: str"
        else:
            # 处理其他数据类型，例如 bytes、float、bool 等
            # ...
            pass

        interface_file_content += f"\n            {parameter_definition}"

    interface
