/**
 * For educational purposes...
 * Idea from: https://gist.github.com/iikuy/8115191
 * --> modified while studying thw world of c++ and threading
**/
#include <thread>
#include <chrono>
#include <iostream>
#include <queue>
#include <mutex>
#include <condition_variable>
#include "ConsumerData.h"

#define DEBUG  0

#if DEBUG
#define LOG_DEBUG(message, args...) \
    fprintf(stdout, message, ## args);
#else
#define LOG_DEBUG(message, args...)
#endif

std::mutex mtex;
std::condition_variable cv;
std::queue<ConsumerData> cdQueue;

bool finished = false;

void producer(int n) {
    int consumer = 0;
	for(int i=0; i<n; ++i) {
		{
            //lock_quard is valid for limited scope
            std::lock_guard<std::mutex> lk(mtex);
            (0==consumer%3)?consumer = 1:consumer++;
            ConsumerData temp_data(consumer, i);
            cdQueue.push(temp_data);
            LOG_DEBUG("++++++++++++++++++++\n");       
			LOG_DEBUG("Producer pushing %d \n",i);
            LOG_DEBUG("++++++++++++++++++++\n");
        }
        // std::this_thread::sleep_for(std::chrono::milliseconds(rand() % 500 + 1));
		cv.notify_all();
	}
	{
		std::lock_guard<std::mutex> lk(mtex);
        finished = true;
        puts("++++++++++++++++++++");
        std::cout << "Producer is done!" << std::endl;
        puts("++++++++++++++++++++");   
	}
	cv.notify_all();
}

void consumer(int x) {
    int consumed = 0;
    int misses = 0;
	while (true) {
        //wait requires unique_lock
        std::unique_lock<std::mutex> lk(mtex);
        cv.wait(lk, []{ return finished || !cdQueue.empty(); });
		while (!cdQueue.empty()) {
            if (cdQueue.front().getId() == x){
                LOG_DEBUG("--------------------\n");
                LOG_DEBUG("Consumer %d consuming %d\n", x, cdQueue.front().getData());
                LOG_DEBUG("--------------------\n");
                consumed++;
                cdQueue.pop();
            }else{
                LOG_DEBUG("--------------------\n");
                LOG_DEBUG("Consumer %d: Not mine! (%d,%d)\n", x, cdQueue.front().getId(), cdQueue.front().getData());
                LOG_DEBUG("--------------------\n");  
                misses++;
                break;              
            }
        }
        
		if (finished && cdQueue.empty()){
            puts("--------------------");
            std::cout << "Consumer " << x << " is done!" <<" Consumed:" << consumed << " misses:" << misses << std::endl;
            puts("--------------------");
            break;
        } 
	}
}

int main() {
    srand (time(NULL));
	std::thread t1(&producer, 100);
	std::thread t2(&consumer, 1);
    std::thread t3(&consumer, 2);
    std::thread t4(&consumer, 3);
    t1.join();
    t2.join();
    t3.join();
    t4.join();
    std::cout << "Main finished!" << std::endl;
    return 1;
}
