#include "test_program.h"

int main(void) {
    func1(1, 2);
    func2(3, 4);
    func3("cs", "cstring");

    return 0;
}

int func1(int a, int b) {
    return a + b;
}
int func2(int a, int b) {
    return a - b;
}
char * func3(char *a, char *b) {
    return NULL;
}