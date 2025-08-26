#ifndef UTILS_H
#define UTILS_H

#include <vector>
#include <string>

namespace Utils {
    std::vector<std::string> splitString(const std::string& str, char delimiter);
    std::string joinStrings(const std::vector<std::string>& strings, const std::string& separator);
    bool isNumber(const std::string& str);
}

#endif // UTILS_H
