# JSON → C++ Optional Structure Auto Generator

이 프로젝트는 **JSON 파일을 입력하면 C++ 구조체(.hpp)를 자동 생성**하는 스크립트입니다.  
생성된 구조체는 **모든 필드가 `std::optional` 처리**되어,  
JSON 필드가 *있어도 되고 없어도 되는* 유연한 구조를 제공합니다.

---

## ✨ 기능 요약

- 모든 JSON 필드를 **자동으로 감지하여 C++ 구조체 생성**
- 모든 구조체 필드를 **std::optional<T>** 로 생성
- nested JSON → nested struct 자동 생성
- vector, int, double, bool, string 등 기본 타입 지원
- JSON 필드 누락 또는 null 모두 자동 처리
- NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE 자동 생성

---

## 📁 파일 구성

```
gen_struct_from_json_optional.py   # JSON→CPP 구조체 자동 생성기
person.json                        # JSON 예제
person.hpp                         # 자동 생성된 헤더 예제
main.cpp                           # optional 안전 처리 C++ 사용 예제
```

---

## 🚀 사용 방법

### 1. JSON → C++ 구조체 생성

```
python gen_struct_from_json_optional.py <입력 JSON> <출력 HPP>
```

### 예시

```
python gen_struct_from_json_optional.py person.json person.hpp
```

또는:

```
python gen_struct_from_json_optional.py all_containers.json AllContainers.hpp
```

---

## 🧩 JSON 예제 (person.json)

```json
{
    "name": "Alice",
    "age": 30,
    "address": {
        "city": "Seoul",
        "street": "Gangnam-daero",
        "zip": 12345
    },
    "tags": ["c++", "json"]
}
```

---

## 🧱 자동 생성된 person.hpp 예제

```cpp
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
```

---

## 🧪 C++ 사용 예제 (main.cpp)

```cpp
#include <iostream>
#include <nlohmann/json.hpp>
#include "person.hpp"

using json = nlohmann::json;

int main()
{
    const char* json_text = R"({
        "name": "Bob",
        "address": { "city": "Busan" }
    })";

    try {
        json j = json::parse(json_text);
        Person p = j.get<Person>();

        std::cout << "name: " << p.name.value_or("(없음)") << "\n";
        std::cout << "age 존재 여부: " << (p.age ? "있음" : "없음") << "\n";

        if (p.address && p.address->city)
            std::cout << "city: " << p.address->city.value() << "\n";
    }
    catch (const json::parse_error& e) {
        std::cerr << "JSON 파싱 오류: " << e.what() << "\n";
    }
    catch (const json::type_error& e) {
        std::cerr << "타입 불일치 오류: " << e.what() << "\n";
    }

    return 0;
}
```

---

## 🔧 Python 스크립트 코드

전체 스크립트는 아래 파일에 포함됩니다:

**gen_struct_from_json_optional.py**

(사용자는 이 스크립트를 그대로 실행하면 됩니다.)

---

## 라이선스

- [LICENSE](LICENSE)

