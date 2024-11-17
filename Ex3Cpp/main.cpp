#include <driver/i2s.h>
#include <Arduino.h>
#include <stdint.h>
#include <iostream>
#include <vector>
#include "IIR.h"
#include "Filter.h"
#include "ADC.h"
using namespace std;

// The 4 high bits are the channel, and the data is inverted
size_t bytes_read;
uint16_t buffer[I2S_DMA_BUF_LEN] = {0};

unsigned long lastTimePrinted;
unsigned long loopTime = 0;

FIRFilter fir(coefs);
IIRFilter iir(num, den);
CircBuffer<double> FirBuf(fir.WinSize);

void setup(){

    Serial.begin(115200);
    i2sInit();

}

void loop(){
    //unsigned long startMicros = ESP.getCycleCount();

    esp_err_t e = i2s_read(I2S_NUM_0, &buffer, sizeof(buffer), &bytes_read, portMAX_DELAY);
    int16_t sample_read = bytes_read/2;
   
    if( e == ESP_OK ){
        for (int s = 0; s < sample_read; ++s){
            FirBuf.insert(uint12_to_Volt(buffer[s]));
            FirBuf.next();
            Serial.println(conv(s,FirBuf,fir.coef));
        }
    }
}
