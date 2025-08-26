#include "utils.h"
#include <sstream>

namespace Utils {
    
    std::vector<std::string> splitString(const std::string& str, char delimiter) {
        std::vector<std::string> result;
        std::stringstream ss(str);
        std::string item;
        
        while (std::getline(ss, item, delimiter)) {
            result.push_back(item);
        }
        
        return result;
    }
    
    std::string joinStrings(const std::vector<std::string>& strings, const std::string& separator) {
        if (strings.empty()) {
            return "";
        }
        
        std::string result = strings[0];
        for (size_t i = 1; i < strings.size(); ++i) {
            result += separator + strings[i];
        }
        
        return result;
    }
    
    bool isNumber(const std::string& str) {
        if (str.empty()) {
            return false;
        }
        
        size_t start = 0;
        if (str[0] == '-' || str[0] == '+') {
            if (str.length() == 1) {
                return false;
            }
            start = 1;
        }
        
        bool hasDecimal = false;
        for (size_t i = start; i < str.length(); ++i) {
            if (str[i] == '.') {
                if (hasDecimal) {
                    return false;
                }
                hasDecimal = true;
            } else if (!std::isdigit(str[i])) {
                return false;
            }
        }
        
        return true;
    }
}
