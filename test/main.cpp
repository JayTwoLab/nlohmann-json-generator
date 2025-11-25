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
        // JSON 파싱 (문법 오류 발생 가능)
        json j = json::parse(json_text);

        // JSON → 구조체 변환 (optional 덕분에 누락된 필드는 nullopt)
        Person p = j.get<Person>();

        // 출력
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
    catch (const std::exception& e) {
        std::cerr << "기타 예외: " << e.what() << "\n";
    }

    return 0;
}
