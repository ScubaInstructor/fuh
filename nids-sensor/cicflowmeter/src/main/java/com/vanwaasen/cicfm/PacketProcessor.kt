package com.vanwaasen.cicfm

import cic.cs.unb.ca.jnetpcap.*
import com.fasterxml.jackson.databind.JsonNode
import java.net.InetAddress

class PacketProcessor()  {

    private val generator = IdGenerator()
    private var firstPacket: Long = 0
    private var lastPacket: Long = 0

    private val flowTimeout =  120L
    private val activityTimeout = 5000L
    private val bidirectional = true
    private val flowGen = FlowGenerator(
        bidirectional,
        flowTimeout,
        activityTimeout
    )

    private var nValid = 0
    private var nTotal = 0
    private var nDiscarded = 0
    private var i = 0

    public fun getIpv4Info(jsonNode: JsonNode): BasicPacketInfo? {
        var packetInfo: BasicPacketInfo? = null

        try {
            var rootNode = jsonNode.path("_source").path("layers")
            var sourceNode = jsonNode.path("_source")

            val ipLayer = rootNode.path("ip")
            packetInfo = BasicPacketInfo(this.generator)
            packetInfo.src = InetAddress.getByName(ipLayer["ip_ip_src"].asText()).address
            packetInfo.dst = InetAddress.getByName(ipLayer["ip_ip_dst"].asText()).address

            packetInfo.jsonRepresentation = jsonNode.toString()
            packetInfo.captureHost = sourceNode["capture_host"].asText()
            packetInfo.captureInterface = sourceNode["capture_interface_name"].asText()

            val frameLayer = rootNode.path("frame")
            val timestamp = (frameLayer["frame_frame_time_epoch"].asDouble() * 1000000).toLong()
            packetInfo.timeStamp = timestamp

            if (this.firstPacket == 0L) this.firstPacket = timestamp / 1000
            this.lastPacket = timestamp / 1000

            // This check needs to be first because ICMP protocol may embed the contents of
            // the original packet (so it will have tcp/udp headers as well).
            val icmpLayer = rootNode.path("icmp")
            val tcpLayer = rootNode.path("tcp")
            val udpLayer = rootNode.path("udp")
            val sctpLayer = rootNode.path("sctp")
            if (!icmpLayer.isMissingNode) {
                packetInfo.protocol = ProtocolEnum.ICMP
                packetInfo.srcPort = 0
                packetInfo.dstPort = 0
                packetInfo.icmpType = icmpLayer["icmp_icmp_type"].asInt()
                packetInfo.icmpCode = icmpLayer["icmp_icmp_code"].asInt()
            } else if (!tcpLayer.isMissingNode) {
                packetInfo.tcpWindow = tcpLayer["tcp_tcp_window_size"].asInt()
                packetInfo.srcPort = tcpLayer["tcp_tcp_src_port"].asInt()
                packetInfo.dstPort = tcpLayer["tcp_tcp_dst_port"].asInt()
                packetInfo.protocol = ProtocolEnum.TCP

                packetInfo.setFlagFIN(tcpLayer["tcp_tcp_flag_fin"].asBoolean())
                packetInfo.setFlagPSH(tcpLayer["tcp_tcp_flag_psh"].asBoolean())
                packetInfo.setFlagURG(tcpLayer["tcp_tcp_flag_urg"].asBoolean())
                packetInfo.setFlagSYN(tcpLayer["tcp_tcp_flag_syn"].asBoolean())
                packetInfo.setFlagACK(tcpLayer["tcp_tcp_flag_ack"].asBoolean())
                packetInfo.setFlagECE(tcpLayer["tcp_tcp_flag_ece"].asBoolean())
                packetInfo.setFlagCWR(tcpLayer["tcp_tcp_flag_cwr"].asBoolean())
                packetInfo.setFlagRST(tcpLayer["tcp_tcp_flag_rst"].asBoolean())
                packetInfo.payloadBytes = tcpLayer["tcp_tcp_payload_length"].asLong()
                packetInfo.headerBytes = tcpLayer["tcp_tcp_header_length"].asLong()

                val tcpRetransmissionDTO = TcpRetransmissionDTO(
                    InetAddress.getByName(ipLayer["ip_ip_src"].asText()).address,
                    tcpLayer["tcp_tcp_seq_num"].asLong(),
                    tcpLayer.path("tcp_tcp_flag_ack").asLong(),
                    tcpLayer["tcp_tcp_payload_length"].asInt(),
                    packetInfo.tcpWindow,
                    packetInfo.timeStamp
                )
                packetInfo.setTcpRetransmissionDTO(tcpRetransmissionDTO)
            } else if (!udpLayer.isMissingNode) {
                packetInfo.srcPort = udpLayer["udp_udp_srcport"].asInt()
                packetInfo.dstPort = udpLayer["udp_udp_dstport"].asInt()
                val totalLength = udpLayer["udp_udp_length"].asInt()
                val payloadLength = totalLength - 8
                packetInfo.payloadBytes = payloadLength.toLong()
                packetInfo.headerBytes = 8L // per specification fixed size
                packetInfo.protocol = ProtocolEnum.UDP
            } else if (!sctpLayer.isMissingNode) {
                packetInfo.srcPort = sctpLayer["sctp_sctp_srcport"].asInt()
                packetInfo.dstPort = sctpLayer["sctp_sctp_srcport"].asInt()
                packetInfo.payloadBytes = sctpLayer["sctp_sctp_payload_length"].asLong()
                packetInfo.headerBytes = sctpLayer["sctp_sctp_header_length"].asLong()
                packetInfo.protocol = ProtocolEnum.SCTP
            }
        } catch (e: java.lang.Exception) {
            e.printStackTrace();
            return null
        }
        return packetInfo
    }
}