#ifndef FILTER_H
#define FILTER_H

#include <vector>
#include <cstdint>
#include "ADC.h"
using namespace std;

template <typename T>
class CircBuffer{

    private:
        vector<T>  vec;
        unsigned int pos;
        unsigned int ins;
        unsigned int VecSize;
    public:

    CircBuffer( unsigned int size ):vec(size,0){
        VecSize = size;
        pos     = -1;
        ins     = 0;
    }

    //Returns next elem and increments pos
    T next(  ){
        return vec[ (++pos)%VecSize ];
    }

    //Returns elem at relative position to the current elem
    T get( int RelPos ){
        RelPos += pos;
        RelPos = RelPos % VecSize;

        if( RelPos < 0 ){
            RelPos = pos + RelPos;
        }

        return vec[RelPos];
    }

    T insert( T val){
        vec[(ins++)%VecSize] = val;
        return val;
    }

};

class IIRFilter{

    private:
        std::vector<double> num;
        std::vector<double> den;
        unsigned int nz; // Number of coef in the numerator
        unsigned int order;
        CircBuffer<double> outBuff;
        CircBuffer<double> sigBuff;

    public:
        unsigned int ord = 0;
    // const unsigned float SampleTime;

    IIRFilter(const std::vector<double> &numerator, const std::vector<double> &denominator)
        : num(numerator),
        den(denominator),
        nz(numerator.size()),
        order(denominator.size()),
        outBuff( order ),
        sigBuff( order ){
        // order   = den.size();
        // nz      = num.size();
        ord = order;
    };

    double ProcessAdHoc( double signal ){
        double aux = 0;
        unsigned int CoefPower;
        sigBuff.insert(signal);
        sigBuff.next();
        outBuff.next();
        
        for (unsigned int index = 0; index < nz; ++index){
            CoefPower = nz - index;
            aux += num[index] * uint12_to_Volt(sigBuff.get(- order + CoefPower));
        }
        for (unsigned int index = 1; index < order; ++index){
            // CoefPower = order - index;
            aux -= den[index] * outBuff.get( - index);
        }

        aux = aux/den[0];
        outBuff.insert( aux );
        return aux;
    }
    
    // The output is Time shifted Ts*order
    // And the output vector has a size = sig.size() - order
    vector<double> ProcessSignal(uint16_t sig[],unsigned int SigSize)
    {

        vector<double> output(order, 0);
        float aux;
        unsigned int CoefPower;

        for (unsigned int SigIndex = order; SigIndex < SigSize; ++SigIndex){
            aux = 0;
            for (unsigned int index = 0; index < nz; ++index){
                CoefPower = nz - index;
                aux += num[index] * uint12_to_Volt(sig[SigIndex - order + CoefPower]);
            }
            for (unsigned int index = 1; index < order; ++index){
                // CoefPower = order - index;
                aux -= den[index] * output[SigIndex - index];
            }
            output.push_back(aux / den[0]);
        }
        output.erase(output.begin(), output.begin() + order);
        return output;
    };
};

double conv( unsigned int pos, CircBuffer<double> sig,vector<double> coef ){
    
    double aux = 0;
    for (unsigned int n = 0; n < coef.size(); ++n){
        aux += sig.get(- n) * coef[n];
    }
    return aux;
}

#endif