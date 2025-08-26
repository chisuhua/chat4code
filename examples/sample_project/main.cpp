#include <iostream>
#include <vector>
#include <string>

class HelloWorld {
private:
    std::string message;
    
public:
    HelloWorld(const std::string& msg) : message(msg) {}
    
    void printMessage() {
        std::cout << message << std::endl;
    }
    
    std::string getMessage() const {
        return message;
    }
};

int main() {
    HelloWorld hello("Hello, World!");
    hello.printMessage();
    return 0;
}
