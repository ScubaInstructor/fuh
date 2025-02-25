package com.vanwaasen.cicfm.flink;

import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.util.Base64;
import java.util.List;

public class PcapMerger {

    private static final int PCAP_MAGIC_NUMBER = 0xa1b2c3d4;
    private static final int PCAP_VERSION_MAJOR = 2;
    private static final int PCAP_VERSION_MINOR = 4;
    private static final int PCAP_TIMEZONE = 0;
    private static final int PCAP_SIGFIGS = 0;
    private static final int PCAP_SNAPLEN = 65535;
    private static final int PCAP_NETWORK = 1; // Ethernet

    public static byte[] mergePcapPackets(List<String> base64Packets) throws Exception {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        // ✅ Write PCAP Global Header (24 bytes)
        ByteBuffer globalHeader = ByteBuffer.allocate(24);
        globalHeader.putInt(PCAP_MAGIC_NUMBER);
        globalHeader.putShort((short) PCAP_VERSION_MAJOR);
        globalHeader.putShort((short) PCAP_VERSION_MINOR);
        globalHeader.putInt(PCAP_TIMEZONE);
        globalHeader.putInt(PCAP_SIGFIGS);
        globalHeader.putInt(PCAP_SNAPLEN);
        globalHeader.putInt(PCAP_NETWORK);
        outputStream.write(globalHeader.array());

        for (int i = 0; i < base64Packets.size(); i++) {
            String base64Packet = base64Packets.get(i);
            byte[] decodedPacket = Base64.getDecoder().decode(base64Packet);

            if (decodedPacket.length < 1) {
                continue;
            }

            int tsSec = (int) (System.currentTimeMillis() / 1000);
            int tsUsec = (int) ((System.currentTimeMillis() % 1000) * 1000);
            int inclLen = decodedPacket.length;
            int origLen = decodedPacket.length;

            ByteBuffer packetHeader = ByteBuffer.allocate(16);
            packetHeader.putInt(tsSec);
            packetHeader.putInt(tsUsec);
            packetHeader.putInt(inclLen);
            packetHeader.putInt(origLen);
            outputStream.write(packetHeader.array());
            outputStream.write(decodedPacket);

        }

        return outputStream.toByteArray();
    }
}

