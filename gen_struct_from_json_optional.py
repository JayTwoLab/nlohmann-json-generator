#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import pathlib

# 구조체 정보를 저장하기 위한 간단한 자료 구조
class StructDef:
    # 구조체 이름과 필드 목록을 보관
    def __init__(self, name):
        self.name = name
        self.fields = []  # (필드이름, C++타입)

    def add_field(self, field_name, field_type):
        self.fields.append((field_name, field_type))


# 파일 이름에서 루트 구조체 이름 추출 (예: person.json → Person)
def root_struct_name_from_filename(filename: str) -> str:
    stem = pathlib.Path(filename).stem
    return to_camel_case(stem)


# JSON 키 이름을 C++ 구조체 이름/타입 이름(PascalCase)로 변환
def to_camel_case(name: str) -> str:
    for ch in ['-', ' ', '.', '/']:
        name = name.replace(ch, '_')
    parts = [p for p in name.split('_') if p]
        # 사용자가 알려준 부분에 대한 예외 처리 included
    if not parts:
        return "GeneratedType"
    return ''.join(p[0].upper() + p[1:] for p in parts)


# JSON 기본 타입 → C++ 타입 매핑
def cpp_type_from_value(key_name: str, value, structs: dict, parent_struct_name: str):
    if isinstance(value, str):
        return "std::string"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "double"
    if value is None:
        return "nlohmann::json"

    if isinstance(value, list):
        # 리스트가 비어 있으면 json 벡터로 처리
        if not value:
            return "std::vector<nlohmann::json>"

        # 첫 번째 non-null 요소의 타입으로 추론
        elem_type = None
        for v in value:
            if v is not None:
                elem_type = cpp_type_from_value(key_name, v, structs, parent_struct_name)
                break
        if elem_type is None:
            elem_type = "nlohmann::json"

        return f"std::vector<{elem_type}>"

    if isinstance(value, dict):
        struct_name = to_camel_case(key_name)

        # 중첩 구조체 생성
        if struct_name not in structs:
            struct_def = StructDef(struct_name)
            structs[struct_name] = struct_def
            for k, v in value.items():
                field_type = cpp_type_from_value(k, v, structs, struct_name)
                struct_def.add_field(k, field_type)
        return struct_name

    # 알 수 없는 타입은 json으로
    return "nlohmann::json"


# JSON 객체에서 루트 구조체 생성
def build_structs_from_json(root_name: str, data, structs: dict):
    if not isinstance(data, dict):
        raise ValueError("루트 JSON은 반드시 object 여야 합니다.")

    root_struct = StructDef(root_name)
    structs[root_name] = root_struct

    for k, v in data.items():
        field_type = cpp_type_from_value(k, v, structs, root_name)
        root_struct.add_field(k, field_type)


# C++ 헤더 파일 생성
def generate_header_code(header_guard: str, structs: dict) -> str:
    lines = []

    lines.append("// 이 파일은 JSON 예제로부터 자동 생성되었습니다.")
    lines.append("// 필요에 따라 수동 수정이 가능합니다.\n")
    lines.append("#pragma once\n")
    lines.append("#include <string>")
    lines.append("#include <vector>")
    lines.append("#include <optional>")
    lines.append("#include <nlohmann/json.hpp>\n")
    lines.append("using json = nlohmann::json;\n")

    # 구조체 정의
    for struct_name, struct_def in structs.items():
        lines.append(f"struct {struct_name} {{")
        for field_name, field_type in struct_def.fields:
            # **모든 필드를 std::optional 로 감싼다**
            lines.append(f"    std::optional<{field_type}> {field_name};")
        lines.append("};\n")

    # NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE 생성
    for struct_name, struct_def in structs.items():
        field_list = ", ".join(n for n, _ in struct_def.fields)
        lines.append(f"NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE({struct_name}, {field_list})")

    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("사용법: python gen_struct_from_json_optional.py <입력 json> <출력 hpp>")
        sys.exit(1)

    json_path = sys.argv[1]
    header_path = sys.argv[2]

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    root_name = root_struct_name_from_filename(json_path)
    header_guard = pathlib.Path(header_path).name.upper().replace('.', '_')

    structs = {}
    build_structs_from_json(root_name, data, structs)

    header_text = generate_header_code(header_guard, structs)

    with open(header_path, "w", encoding="utf-8") as f:
        f.write(header_text)

    print(f"{header_path} 파일이 생성되었습니다.")
    print("루트 구조체:", root_name)


if __name__ == "__main__":
    main()
