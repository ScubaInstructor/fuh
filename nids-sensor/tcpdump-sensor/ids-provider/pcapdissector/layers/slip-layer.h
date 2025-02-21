//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef SLIP_LAYER_H
#define SLIP_LAYER_H

#include "ids-provider/pcapdissector/layer.h"
#include <packet.h>
#include <stdint.h>
#include <stddef.h>


// Function to dissect SLIP layer
int dissect_slip(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);

#endif // SLIP_LAYER_H

