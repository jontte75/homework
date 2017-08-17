#include <iostream>
#include <thread>
#include <chrono>
#include "ThreadGuard.h"

using namespace std;

void func1(int x){
    std::this_thread::sleep_for(chrono::milliseconds(5000));
    cout << "func1 called " << "with value " << x << endl;
}

class MyClass{
public:
    MyClass(){puts("MyClass CTOR!");}
    ~MyClass(){puts("MyClass DTOR!");}
    void operator()(int & x){
        std::this_thread::sleep_for(chrono::milliseconds(6000));
        printf("Moro from class function call operator! %d\n",x);
    }
};

void crash(){
    throw std::runtime_error("Oops...");
}

int main(){
    int x = 10;
    std::thread thread1(func1,x);
    ThreadGuard tg1(thread1);
 
    MyClass mc1;
    std::thread thread2(mc1, std::ref(x));
    ThreadGuard tg2(thread2);
    
    x = 55;
    //crash();

    thread1.join();
    thread2.detach();

    cout << "This is main" << endl;

    cout << "Hit enter!" << endl;
    (void)getchar();
}