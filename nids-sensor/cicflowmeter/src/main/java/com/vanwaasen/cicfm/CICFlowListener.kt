package com.vanwaasen.cicfm

import cic.cs.unb.ca.jnetpcap.BasicFlow

interface CICFlowListener {
    fun onFlowGenerated(flow: BasicFlow)
}