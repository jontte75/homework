#ifndef _CONSUMER_DATA_H
#define _CONSUMER_DATA_H

class ConsumerData{
    int id;
    int data;
    ConsumerData(){}
public:
    ConsumerData(int _id, int _data):id(_id),data(_data) {}
    ~ConsumerData(){}
    int getId() {return id;}
    int getData() {return data;}
};
#endif