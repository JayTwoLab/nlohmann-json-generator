// 이 파일은 JSON 예제로부터 자동 생성되었습니다.
// 필요에 따라 수동 수정이 가능합니다.

#pragma once
#include <string>
#include <vector>
#include <optional>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

struct Person {
    std::optional<std::string> name;
    std::optional<int> age;
    std::optional<Address> address;
    std::optional<std::vector<std::string>> tags;
};

struct Address {
    std::optional<std::string> city;
    std::optional<std::string> street;
    std::optional<int> zip;
};

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Person, name, age, address, tags)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Address, city, street, zip)
