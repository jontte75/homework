#ifndef _THREADGUARD_H
#define _THREADGUARD_H

#include <thread>

class ThreadGuard {
    std::thread & t;
public:
    ThreadGuard(std::thread & th): t(th)
    {puts("ThreadGuard CTOR called");}

    ~ThreadGuard(){
        if (t.joinable()){
            puts("ThreadGuard DTOR, Join called");
            t.join();
        }else{
            puts("ThreadGuard DTOR, Join NOT called");
        }
    }
};

#endif