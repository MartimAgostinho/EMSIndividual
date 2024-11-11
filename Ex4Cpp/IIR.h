#ifndef IIR_H
#define IIR_H

#include <vector>
#include "Filter.h"

vector<double> num{
        0.8,
        6*0.8,
        0.8
};
vector<double> den{
        1,
        -0.36953, 
        0.19582
        };
IIRFilter f1(num,den); 

#endif