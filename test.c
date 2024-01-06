#include <stdio.h>

void testprint();

void main_test(int p1, int p2){
    int p3 = p1 + p2;
    printf("%s - %s(%d) in printf (%d)\n", __FILE__, __func__, __LINE__, p3);
}

int main()
{
    int para1 = 1;
    int para2 = 2;
    testprint();
    main_test(para1, para2);
    printf("%s - %s(%d) in printf \n", __FILE__, __func__, __LINE__);
    return 0;
}