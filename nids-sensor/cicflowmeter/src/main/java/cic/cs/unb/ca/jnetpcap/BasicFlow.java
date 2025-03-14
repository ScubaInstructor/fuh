package cic.cs.unb.ca.jnetpcap;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;
import org.jnetpcap.packet.format.FormatUtils;

import java.util.*;

import static com.fasterxml.jackson.module.kotlin.ExtensionsKt.jacksonObjectMapper;

public class BasicFlow {

    private final static String separator = ",";
    private SummaryStatistics fwdPktStats = null;
    private SummaryStatistics bwdPktStats = null;
    private List<BasicPacketInfo> forward = null;
    private List<String> forwardPackets = null;
    private List<BasicPacketInfo> backward = null;
    private List<String> backwardPackets = null;

    private long forwardBytes;
    private long backwardBytes;
    private long fHeaderBytes;
    private long bHeaderBytes;

    // Is always the value true in this application
    private boolean isBidirectional;

    private HashMap<String, MutableInt> flagCounts;

    private int fPSH_cnt;
    private int bPSH_cnt;
    private int fURG_cnt;
    private int bURG_cnt;
    private int bRST_cnt;
    private int fRST_cnt;
    private int fFIN_cnt;
    private int bFIN_cnt;

    private long Act_data_pkt_forward;
    private long Act_data_pkt_backward;
    private long min_seg_size_forward;
    private long min_seg_size_backward;
    private int Init_Win_bytes_forward = 0;
    private int Init_Win_bytes_backward = 0;


    private byte[] src;
    private byte[] dst;
    private int srcPort;
    private int dstPort;
    private ProtocolEnum protocol;
    private long flowStartTime;
    private long startActiveTime;
    private long endActiveTime;
    private String flowId = null;

    private SummaryStatistics flowIAT = null;
    private SummaryStatistics forwardIAT = null;
    private SummaryStatistics backwardIAT = null;
    private SummaryStatistics flowLengthStats = null;
    private SummaryStatistics flowActive = null;
    private SummaryStatistics flowIdle = null;

    private long flowLastSeen;
    private long forwardLastSeen;
    private long backwardLastSeen;
    private long activityTimeout;
    private long sfLastPacketTS = -1;
    private int sfCount = 0;
    private long sfAcHelper = -1;
    //////////////////////////////
    private long fbulkDuration = 0;
    private long fbulkPacketCount = 0;
    private long fbulkSizeTotal = 0;
    private long fbulkStateCount = 0;
    private long fbulkPacketCountHelper = 0;
    private long fbulkStartHelper = 0;
    private long fbulkSizeHelper = 0;
    private long flastBulkTS = 0;
    private long bbulkDuration = 0;
    private long bbulkPacketCount = 0;
    private long bbulkSizeTotal = 0;
    private long bbulkStateCount = 0;
    private long bbulkPacketCountHelper = 0;
    private long bbulkStartHelper = 0;
    private long bbulkSizeHelper = 0;
    private long blastBulkTS = 0;

    private int fwdTcpRetransCnt = 0;
    private int bwdTcpRetransCnt = 0;
    private Set<TcpRetransmissionDTO> tcpPacketsSeen;

    private String captureHost = "unknwon";
    private String captureInterface = "unknown";

    // The flow timeout is dependent on the user configuration and is unable to capture proper
    // context in extended TCP connections. This field will help identify whether a flow is
    // part of an extended TCP connection.
    private long cumulativeConnectionDuration;

    //To keep track of TCP connection teardown, or an RST packet in one direction.
    private TcpFlowState tcpFlowState;

    // ICMP fields
    private int icmpCode = -1;
    private int icmpType = -1;

    public BasicFlow(boolean isBidirectional, BasicPacketInfo packet, byte[] flowSrc, byte[] flowDst, int flowSrcPort,
                     int flowDstPort, long activityTimeout) {
        super();
        this.activityTimeout = activityTimeout;
        this.initParameters();
        this.isBidirectional = isBidirectional;
        this.src = flowSrc;
        this.dst = flowDst;
        this.srcPort = flowSrcPort;
        this.dstPort = flowDstPort;
        this.firstPacket(packet);
    }

    public BasicFlow(boolean isBidirectional, BasicPacketInfo packet, byte[] flowSrc, byte[] flowDst, int flowSrcPort,
            int flowDstPort, long activityTimeout, Set<TcpRetransmissionDTO> tcpPacketsSeen) {
        super();
        this.activityTimeout = activityTimeout;
        this.initParameters();
        this.isBidirectional = isBidirectional;
        this.src = flowSrc;
        this.dst = flowDst;
        this.srcPort = flowSrcPort;
        this.dstPort = flowDstPort;
        this.tcpPacketsSeen = tcpPacketsSeen;
        this.firstPacket(packet);
    }


    public BasicFlow(boolean isBidirectional, BasicPacketInfo packet, long activityTimeout) {
        super();
        this.activityTimeout = activityTimeout;
        this.initParameters();
        this.isBidirectional = isBidirectional;
        this.firstPacket(packet);
    }

    public BasicFlow(BasicPacketInfo packet, long activityTimeout) {
        super();
        this.activityTimeout = activityTimeout;
        this.initParameters();
        this.isBidirectional = true;
        firstPacket(packet);
    }


    public void initParameters() {
        this.forward = new ArrayList<BasicPacketInfo>();
        this.backward = new ArrayList<BasicPacketInfo>();
        this.flowIAT = new SummaryStatistics();
        this.forwardIAT = new SummaryStatistics();
        this.backwardIAT = new SummaryStatistics();
        this.flowActive = new SummaryStatistics();
        this.flowIdle = new SummaryStatistics();
        this.flowLengthStats = new SummaryStatistics();
        this.fwdPktStats = new SummaryStatistics();
        this.bwdPktStats = new SummaryStatistics();
        this.flagCounts = new HashMap<String, MutableInt>();
        initFlags();
        this.forwardBytes = 0L;
        this.backwardBytes = 0L;
        this.startActiveTime = 0L;
        this.endActiveTime = 0L;
        this.src = null;
        this.dst = null;
        this.fPSH_cnt = 0;
        this.bPSH_cnt = 0;
        this.fURG_cnt = 0;
        this.bURG_cnt = 0;
        this.fFIN_cnt = 0;
        this.bFIN_cnt = 0;
        this.fHeaderBytes = 0L;
        this.bHeaderBytes = 0L;
        this.cumulativeConnectionDuration = 0L;
        this.tcpFlowState = null;
        this.tcpPacketsSeen = new HashSet<TcpRetransmissionDTO>();
    }

    public void firstPacket(BasicPacketInfo packet) {
        
        if (this.src == null) {
            this.src = packet.getSrc();
            this.srcPort = packet.getSrcPort();
        }
        if (this.dst == null) {
            this.dst = packet.getDst();
            this.dstPort = packet.getDstPort();
        }

        updateFlowBulk(packet);

        checkFlags(packet);

        this.endActiveTime = packet.getTimeStamp();
        this.flowStartTime = packet.getTimeStamp();
        this.flowLastSeen = packet.getTimeStamp();
        this.startActiveTime = packet.getTimeStamp();
        detectUpdateSubflows(packet);
        this.flowLengthStats.addValue((double) packet.getPayloadBytes());

        if (Arrays.equals(this.src, packet.getSrc())) {
            this.min_seg_size_forward = packet.getHeaderBytes();
            Init_Win_bytes_forward = packet.getTCPWindow();
            this.fwdPktStats.addValue((double) packet.getPayloadBytes());
            this.fHeaderBytes = packet.getHeaderBytes();
            this.forwardLastSeen = packet.getTimeStamp();
            this.forwardBytes += packet.getPayloadBytes();
            this.forward.add(packet);
            if (packet.getPayloadBytes() >= 1) {
                this.Act_data_pkt_forward++;
            }
            if (packet.hasFlagPSH()) {
                this.fPSH_cnt++;
            }
            if (packet.hasFlagURG()) {
                this.fURG_cnt++;
            }
            if (packet.hasFlagFIN()) {
                this.fFIN_cnt++;
            }
            if (packet.hasFlagRST()) {
                this.fRST_cnt++;
            }
        } else {
            this.min_seg_size_backward = packet.getHeaderBytes();
            Init_Win_bytes_backward = packet.getTCPWindow();
            this.bwdPktStats.addValue((double) packet.getPayloadBytes());
            this.bHeaderBytes = packet.getHeaderBytes();
            this.backwardLastSeen = packet.getTimeStamp();
            this.backwardBytes += packet.getPayloadBytes();
            this.backward.add(packet);
            if (packet.getPayloadBytes() >= 1) {
                this.Act_data_pkt_backward++;
            }
            if (packet.hasFlagPSH()) {
                this.bPSH_cnt++;
            }
            if (packet.hasFlagURG()) {
                this.bURG_cnt++;
            }
            if (packet.hasFlagFIN()) {
                this.bFIN_cnt++;
            }
            if (packet.hasFlagRST()) {
                this.bRST_cnt++;
            }
        }
        this.protocol = packet.getProtocol();
        this.icmpCode = packet.getIcmpCode();
        this.icmpType = packet.getIcmpType();
        this.flowId = packet.getFlowId();
        this.captureHost = packet.getCaptureHost();
        this.captureInterface = packet.getCaptureInterface();
        handleTcpRetransmissionFields(packet);
    }

    /***
     * The retransmission mechanism is crude, and relies on the fact that the fields in the TcpRetransmissionDTO
     * class are unique. This is not a perfect solution, but it should be good enough for detection of very obvious
     * TCP retransmissions.
     * @param packet
     */
    private void handleTcpRetransmissionFields(BasicPacketInfo packet) {
        if (this.protocol == ProtocolEnum.TCP) {
            TcpRetransmissionDTO tcpRetransmissionDTO = packet.tcpRetransmissionDTO();
            // If the element was successfully added to the hashset, then it has not been seen
            // before, and is not a retransmission.
            boolean isRetransmission = !(this.tcpPacketsSeen.add(tcpRetransmissionDTO));
            if (isRetransmission) {
                // check if the packet is a forward packet
                if (Arrays.equals(this.src, packet.getSrc())) {
                    // increment the forward retransmission count
                    this.fwdTcpRetransCnt++;
                } else {
                    // increment the backward retransmission count
                    this.bwdTcpRetransCnt++;
                }
            }
        }
    }

    public void addPacket(BasicPacketInfo packet) {
        updateFlowBulk(packet);
        detectUpdateSubflows(packet);
        checkFlags(packet);
        handleTcpRetransmissionFields(packet);
        long currentTimestamp = packet.getTimeStamp();
        if (isBidirectional) {
            this.flowLengthStats.addValue((double) packet.getPayloadBytes());
            if (Arrays.equals(this.src, packet.getSrc())) {
                if (packet.getPayloadBytes() >= 1) {
                    this.Act_data_pkt_forward++;
                }
                this.fwdPktStats.addValue((double) packet.getPayloadBytes());
                this.fHeaderBytes += packet.getHeaderBytes();
                this.forward.add(packet);
                this.forwardBytes += packet.getPayloadBytes();
                if (this.forward.size() > 1)
                    this.forwardIAT.addValue(currentTimestamp - this.forwardLastSeen);
                this.forwardLastSeen = currentTimestamp;
                this.min_seg_size_forward = Math.min(packet.getHeaderBytes(), this.min_seg_size_forward);
                if (packet.hasFlagPSH()) {
                    this.fPSH_cnt++;
                }
                if (packet.hasFlagURG()) {
                    this.fURG_cnt++;
                }
                if (packet.hasFlagFIN()) {
                    this.fFIN_cnt++;
                }
                if (packet.hasFlagRST()) {
                    this.fRST_cnt++;
                }
            } else {
                if (packet.getPayloadBytes() >= 1) {
                    this.Act_data_pkt_backward++;
                }
                this.bwdPktStats.addValue((double) packet.getPayloadBytes());
                // set Init_win_bytes_backward if not been set. The set logic isn't 100%
                // accurate, since it technically takes the first non-zero value, but should
                // be good enough for most cases.
                if (Init_Win_bytes_backward == 0) {
                    Init_Win_bytes_backward = packet.getTCPWindow();
                }
                this.bHeaderBytes += packet.getHeaderBytes();
                this.backward.add(packet);
                this.backwardBytes += packet.getPayloadBytes();
                if (this.backward.size() > 1)
                    this.backwardIAT.addValue(currentTimestamp - this.backwardLastSeen);
                this.backwardLastSeen = currentTimestamp;
                this.min_seg_size_backward = Math.min(packet.getHeaderBytes(), this.min_seg_size_backward);
                if (packet.hasFlagPSH()) {
                    this.bPSH_cnt++;
                }
                if (packet.hasFlagURG()) {
                    this.bURG_cnt++;
                }
                if (packet.hasFlagFIN()) {
                    this.bFIN_cnt++;
                }
                if (packet.hasFlagRST()) {
                    this.bRST_cnt++;
                }
            }
        } else {
            if (packet.getPayloadBytes() >= 1) {
                this.Act_data_pkt_forward++;
            }
            this.fwdPktStats.addValue((double) packet.getPayloadBytes());
            this.flowLengthStats.addValue((double) packet.getPayloadBytes());
            this.fHeaderBytes += packet.getHeaderBytes();
            this.forward.add(packet);
            this.forwardBytes += packet.getPayloadBytes();
            this.forwardIAT.addValue(currentTimestamp - this.forwardLastSeen);
            this.forwardLastSeen = currentTimestamp;
            this.min_seg_size_forward = Math.min(packet.getHeaderBytes(), this.min_seg_size_forward);
        }

        this.flowIAT.addValue(packet.getTimeStamp() - this.flowLastSeen);
        this.flowLastSeen = packet.getTimeStamp();

    }

    public double getfPktsPerSecond() {
        long duration = this.flowLastSeen - this.flowStartTime;
        if (duration > 0) {
            return (this.forward.size() / ((double) duration / 1000000L));
        } else
            return 0;
    }

    public double getbPktsPerSecond() {
        long duration = this.flowLastSeen - this.flowStartTime;
        if (duration > 0) {
            return (this.backward.size() / ((double) duration / 1000000L));
        } else
            return 0;
    }

    public double getDownUpRatio() {
        if (this.forward.size() > 0) {
            return ((double)this.backward.size())/this.forward.size();
        }
        return 0;
    }

    public double getAvgPacketSize() {
        if (this.packetCount() > 0) {
            return (this.flowLengthStats.getSum() / this.packetCount());
        }
        return 0;
    }

    public double fAvgSegmentSize() {
        if (this.forward.size() != 0)
            return (this.fwdPktStats.getSum() / (double) this.forward.size());
        return 0;
    }

    public double bAvgSegmentSize() {
        if (this.backward.size() != 0)
            return (this.bwdPktStats.getSum() / (double) this.backward.size());
        return 0;
    }

    public void initFlags() {
        flagCounts.put("FIN", new MutableInt());
        flagCounts.put("SYN", new MutableInt());
        flagCounts.put("RST", new MutableInt());
        flagCounts.put("PSH", new MutableInt());
        flagCounts.put("ACK", new MutableInt());
        flagCounts.put("URG", new MutableInt());
        flagCounts.put("CWR", new MutableInt());
        flagCounts.put("ECE", new MutableInt());
    }

    public void checkFlags(BasicPacketInfo packet) {
        if (packet.hasFlagFIN()) {
            //MutableInt count1 = flagCounts.get("FIN");
            //count1.increment();
            flagCounts.get("FIN").increment();
        }
        if (packet.hasFlagSYN()) {
            //MutableInt count2 = flagCounts.get("SYN");
            //count2.increment();
            flagCounts.get("SYN").increment();
        }
        if (packet.hasFlagRST()) {
            //MutableInt count3 = flagCounts.get("RST");
            //count3.increment();
            flagCounts.get("RST").increment();
        }
        if (packet.hasFlagPSH()) {
            //MutableInt count4 = flagCounts.get("PSH");
            //count4.increment();
            flagCounts.get("PSH").increment();
        }
        if (packet.hasFlagACK()) {
            //MutableInt count5 = flagCounts.get("ACK");
            //count5.increment();
            flagCounts.get("ACK").increment();
        }
        if (packet.hasFlagURG()) {
            //MutableInt count6 = flagCounts.get("URG");
            //count6.increment();
            flagCounts.get("URG").increment();
        }
        if (packet.hasFlagCWR()) {
            //MutableInt count7 = flagCounts.get("CWR");
            //count7.increment();
            flagCounts.get("CWR").increment();
        }
        if (packet.hasFlagECE()) {
            //MutableInt count8 = flagCounts.get("ECE");
            //count8.increment();
            flagCounts.get("ECE").increment();
        }
    }

    public double getSflow_fbytes() {
        if (sfCount <= 0) return 0;
        return (double) this.forwardBytes / sfCount;
    }

    public double getSflow_fpackets() {
        if (sfCount <= 0) return 0;
        return (double) this.forward.size() / sfCount;
    }

    public double getSflow_bbytes() {
        if (sfCount <= 0) return 0;
        return (double) this.backwardBytes / sfCount;
    }

    public double getSflow_bpackets() {
        if (sfCount <= 0) return 0;
        return (double) this.backward.size() / sfCount;
    }

    void detectUpdateSubflows(BasicPacketInfo packet) {
        if (sfLastPacketTS == -1) {
            sfLastPacketTS = packet.getTimeStamp();
            sfAcHelper = packet.getTimeStamp();
        }
        //System.out.print(" - "+(packet.timeStamp - sfLastPacketTS));
        if(((packet.getTimeStamp() - sfLastPacketTS)/(double)1000000)  > 1.0){
            sfCount++;
            long lastSFduration = packet.getTimeStamp() - sfAcHelper;
            updateActiveIdleTime(packet.getTimeStamp(), this.activityTimeout);
            sfAcHelper = packet.getTimeStamp();
        }

        sfLastPacketTS = packet.getTimeStamp();
    }

    public void updateFlowBulk(BasicPacketInfo packet) {
        if (Arrays.equals(this.src, packet.getSrc())) {
            updateForwardBulk(packet, blastBulkTS);
        } else {
            updateBackwardBulk(packet,flastBulkTS);
        }
    }

    public void updateForwardBulk(BasicPacketInfo packet, long tsOflastBulkInOther) {

        long size = packet.getPayloadBytes();
        if (tsOflastBulkInOther > fbulkStartHelper) fbulkStartHelper = 0;
        if (size <= 0) return;

        packet.getPayloadPacket();

        if (fbulkStartHelper == 0) {
            fbulkStartHelper = packet.getTimeStamp();
            fbulkPacketCountHelper = 1;
            fbulkSizeHelper = size;
            flastBulkTS = packet.getTimeStamp();
        } //possible bulk
        else {
            // Too much idle time?
            if (((packet.getTimeStamp() - flastBulkTS) / (double) 1000000) > 1.0) {
                fbulkStartHelper = packet.getTimeStamp();
                flastBulkTS = packet.getTimeStamp();
                fbulkPacketCountHelper = 1;
                fbulkSizeHelper = size;
            }// Add to bulk
            else {
                fbulkPacketCountHelper += 1;
                fbulkSizeHelper += size;
                //New bulk
                if (fbulkPacketCountHelper == 4) {
                    fbulkStateCount += 1;
                    fbulkPacketCount += fbulkPacketCountHelper;
                    fbulkSizeTotal += fbulkSizeHelper;
                    fbulkDuration += packet.getTimeStamp() - fbulkStartHelper;
                } //Continuation of existing bulk
                else if (fbulkPacketCountHelper > 4) {
                    fbulkPacketCount += 1;
                    fbulkSizeTotal += size;
                    fbulkDuration += packet.getTimeStamp() - flastBulkTS;
                }
                flastBulkTS = packet.getTimeStamp();
            }
        }
    }

    public void updateBackwardBulk(BasicPacketInfo packet, long tsOflastBulkInOther) {
		/*bAvgBytesPerBulk =0;
		bbulkSizeTotal=0;
		bbulkStateCount=0;*/
        long size = packet.getPayloadBytes();
        if (tsOflastBulkInOther > bbulkStartHelper) bbulkStartHelper = 0;
        if (size <= 0) return;

        packet.getPayloadPacket();

        if (bbulkStartHelper == 0) {
            bbulkStartHelper = packet.getTimeStamp();
            bbulkPacketCountHelper = 1;
            bbulkSizeHelper = size;
            blastBulkTS = packet.getTimeStamp();
        } //possible bulk
        else {
            // Too much idle time?
            if (((packet.getTimeStamp() - blastBulkTS) / (double) 1000000) > 1.0) {
                bbulkStartHelper = packet.getTimeStamp();
                blastBulkTS = packet.getTimeStamp();
                bbulkPacketCountHelper = 1;
                bbulkSizeHelper = size;
            }// Add to bulk
            else {
                bbulkPacketCountHelper += 1;
                bbulkSizeHelper += size;
                //New bulk
                if (bbulkPacketCountHelper == 4) {
                    bbulkStateCount += 1;
                    bbulkPacketCount += bbulkPacketCountHelper;
                    bbulkSizeTotal += bbulkSizeHelper;
                    bbulkDuration += packet.getTimeStamp() - bbulkStartHelper;
                } //Continuation of existing bulk
                else if (bbulkPacketCountHelper > 4) {
                    bbulkPacketCount += 1;
                    bbulkSizeTotal += size;
                    bbulkDuration += packet.getTimeStamp() - blastBulkTS;
                }
                blastBulkTS = packet.getTimeStamp();
            }
        }

    }

    public long fbulkStateCount() {
        return fbulkStateCount;
    }

    public long fbulkSizeTotal() {
        return fbulkSizeTotal;
    }

    public long fbulkPacketCount() {
        return fbulkPacketCount;
    }

    public long fbulkDuration() {
        return fbulkDuration;
    }

    public double fbulkDurationInSecond() {
        return fbulkDuration / (double) 1000000;
    }


    //Client average bytes per bulk
    public double fAvgBytesPerBulk() {
        if (this.fbulkStateCount() != 0)
            return ((double) this.fbulkSizeTotal() / this.fbulkStateCount());
        return 0;
    }


    //Client average packets per bulk
    public double fAvgPacketsPerBulk() {
        if (this.fbulkStateCount() != 0)
            return ((double) this.fbulkPacketCount() / this.fbulkStateCount());
        return 0;
    }


    //Client average bulk rate
    public double fAvgBulkRate() {
        if (this.fbulkDuration() != 0)
            return ((double) this.fbulkSizeTotal() / this.fbulkDurationInSecond());
        return 0;
    }


    //new features server
    public long bbulkPacketCount() {
        return bbulkPacketCount;
    }

    public long bbulkStateCount() {
        return bbulkStateCount;
    }

    public long bbulkSizeTotal() {
        return bbulkSizeTotal;
    }

    public long bbulkDuration() {
        return bbulkDuration;
    }

    public double bbulkDurationInSecond() {
        return bbulkDuration / (double) 1000000;
    }

    //Server average bytes per bulk
    public double bAvgBytesPerBulk() {
        if (this.bbulkStateCount() != 0)
            return ((double) this.bbulkSizeTotal() / this.bbulkStateCount());
        return 0;
    }

    //Server average packets per bulk
    public double bAvgPacketsPerBulk() {
        if (this.bbulkStateCount() != 0)
            return ((double) this.bbulkPacketCount() / this.bbulkStateCount());
        return 0;
    }

    //Server average bulk rate
    public double bAvgBulkRate() {
        if (this.bbulkDuration() != 0)
            return ((double) this.bbulkSizeTotal() / this.bbulkDurationInSecond());
        return 0;
    }

    ////////////////////////////


    public void updateActiveIdleTime(long currentTime, long threshold) {
        if ((currentTime - this.endActiveTime) > threshold) {
            if ((this.endActiveTime - this.startActiveTime) > 0) {
                this.flowActive.addValue(this.endActiveTime - this.startActiveTime);
            }
            this.flowIdle.addValue(currentTime - this.endActiveTime);
            this.startActiveTime = currentTime;
            this.endActiveTime = currentTime;
        } else {
            this.endActiveTime = currentTime;
        }
    }

    public void endActiveIdleTime(long currentTime, long threshold, long flowTimeOut, boolean isFlagEnd) {

        if ((this.endActiveTime - this.startActiveTime) > 0) {
            this.flowActive.addValue(this.endActiveTime - this.startActiveTime);
        }

        if (!isFlagEnd && ((flowTimeOut - (this.endActiveTime - this.flowStartTime)) > 0)) {
            this.flowIdle.addValue(flowTimeOut - (this.endActiveTime - this.flowStartTime));
        }
    }

    public String dumpFlowBasedFeatures() {
        String dump = "";
        dump += this.flowId + ",";
        dump += FormatUtils.ip(src) + ",";
        dump += getSrcPort() + ",";
        dump += FormatUtils.ip(dst) + ",";
        dump += getDstPort() + ",";
        dump += getProtocol().val + ",";
        //dump+=this.flowStartTime+",";
        dump += DateFormatter.parseDateFromLong(this.flowStartTime / 1000L, "dd/MM/yyyy hh:mm:ss") + ",";
        long flowDuration = this.flowLastSeen - this.flowStartTime;
        dump += flowDuration + ",";
        dump += this.fwdPktStats.getN() + ",";
        dump += this.bwdPktStats.getN() + ",";
        dump += this.fwdPktStats.getSum() + ",";
        dump += this.bwdPktStats.getSum() + ",";
        if (fwdPktStats.getN() > 0L) {
            dump += this.fwdPktStats.getMax() + ",";
            dump += this.fwdPktStats.getMin() + ",";
            dump += this.fwdPktStats.getMean() + ",";
            dump += this.fwdPktStats.getStandardDeviation() + ",";
        } else {
            dump += "0,0,0,0,";
        }
        if (bwdPktStats.getN() > 0L) {
            dump += this.bwdPktStats.getMax() + ",";
            dump += this.bwdPktStats.getMin() + ",";
            dump += this.bwdPktStats.getMean() + ",";
            dump += this.bwdPktStats.getStandardDeviation() + ",";
        } else {
            dump += "0,0,0,0,";
        }
        // flow duration is in microseconds, therefore packets per seconds = packets / (duration/1000000)
        dump += ((double) (this.forwardBytes + this.backwardBytes)) / ((double) flowDuration / 1000000L) + ",";
        dump += ((double) packetCount()) / ((double) flowDuration / 1000000L) + ",";
        dump += this.flowIAT.getMean() + ",";
        dump += this.flowIAT.getStandardDeviation() + ",";
        dump += this.flowIAT.getMax() + ",";
        dump += this.flowIAT.getMin() + ",";
        if (this.forward.size() > 1) {
            dump += this.forwardIAT.getSum() + ",";
            dump += this.forwardIAT.getMean() + ",";
            dump += this.forwardIAT.getStandardDeviation() + ",";
            dump += this.forwardIAT.getMax() + ",";
            dump += this.forwardIAT.getMin() + ",";
        } else {
            dump += "0,0,0,0,0,";
        }
        if (this.backward.size() > 1) {
            dump += this.backwardIAT.getSum() + ",";
            dump += this.backwardIAT.getMean() + ",";
            dump += this.backwardIAT.getStandardDeviation() + ",";
            dump += this.backwardIAT.getMax() + ",";
            dump += this.backwardIAT.getMin() + ",";
        } else {
            dump += "0,0,0,0,0,";
        }

        dump += this.fPSH_cnt + ",";
        dump += this.bPSH_cnt + ",";
        dump += this.fURG_cnt + ",";
        dump += this.bURG_cnt + ",";

        dump += this.fHeaderBytes + ",";
        dump += this.bHeaderBytes + ",";
        dump += getfPktsPerSecond() + ",";
        dump += getbPktsPerSecond() + ",";

        if (this.forward.size() > 0 || this.backward.size() > 0) {
            dump += this.flowLengthStats.getMin() + ",";
            dump += this.flowLengthStats.getMax() + ",";
            dump += this.flowLengthStats.getMean() + ",";
            dump += this.flowLengthStats.getStandardDeviation() + ",";
            dump += flowLengthStats.getVariance() + ",";
        } else {
            dump += "0,0,0,0,";
        }

        for (String key : flagCounts.keySet()) {
            dump += flagCounts.get(key).value + ",";
        }

        dump += getDownUpRatio() + ",";
        dump += getAvgPacketSize() + ",";
        dump += fAvgSegmentSize() + ",";
        dump += bAvgSegmentSize() + ",";
        dump += this.fHeaderBytes + ",";  //this feature is duplicated


        dump += fAvgBytesPerBulk() + ",";
        dump += fAvgPacketsPerBulk() + ",";
        dump += fAvgBulkRate() + ",";
        dump += fAvgBytesPerBulk() + ",";
        dump += bAvgPacketsPerBulk() + ",";
        dump += bAvgBulkRate() + ",";

        dump += getSflow_fpackets() + ",";
        dump += getSflow_fbytes() + ",";
        dump += getSflow_bpackets() + ",";
        dump += getSflow_bbytes() + ",";

        dump += this.Init_Win_bytes_forward + ",";
        dump += this.Init_Win_bytes_backward + ",";
        dump += this.Act_data_pkt_forward + ",";
        dump += this.Act_data_pkt_forward + ",";
        dump += this.min_seg_size_forward + ",";
        dump += this.min_seg_size_backward + ",";

        if (this.flowActive.getN() > 0) {
            dump += this.flowActive.getMean() + ",";
            dump += this.flowActive.getStandardDeviation() + ",";
            dump += this.flowActive.getMax() + ",";
            dump += this.flowActive.getMin() + ",";
        } else {
            dump += "0,0,0,0,";
        }

        if (this.flowIdle.getN() > 0) {
            dump += this.flowIdle.getMean() + ",";
            dump += this.flowIdle.getStandardDeviation() + ",";
            dump += this.flowIdle.getMax() + ",";
            dump += this.flowIdle.getMin();
        } else {
            dump += "0,0,0,0";
        }
        dump += "," + getLabel();

		/*if(FormatUtils.ip(src).equals("147.32.84.165") | FormatUtils.ip(dst).equals("147.32.84.165")){
			dump+=",BOTNET";
		}
		else{
			dump+=",BENIGN";
		} */
        /////////////////////////////////
        return dump;
    }

    public int packetCount() {
        if (isBidirectional) {
            return (this.forward.size() + this.backward.size());
        } else {
            return this.forward.size();
        }
    }

    public List<BasicPacketInfo> getForward() {
        return new ArrayList<>(forward);
    }

    public void setForward(List<BasicPacketInfo> forward) {
        this.forward = forward;
    }

    public List<BasicPacketInfo> getBackward() {
        return new ArrayList<>(backward);
    }

    public void setBackward(List<BasicPacketInfo> backward) {
        this.backward = backward;
    }

    public boolean isBidirectional() {
        return isBidirectional;
    }

    public void setBidirectional(boolean isBidirectional) {
        this.isBidirectional = isBidirectional;
    }

    public byte[] getSrc() {
        return Arrays.copyOf(src, src.length);
    }

    public void setSrc(byte[] src) {
        this.src = src;
    }

    public byte[] getDst() {
        return Arrays.copyOf(dst, dst.length);
    }

    public void setDst(byte[] dst) {
        this.dst = dst;
    }

    public int getSrcPort() {
        return srcPort;
    }

    public void setSrcPort(int srcPort) {
        this.srcPort = srcPort;
    }

    public int getDstPort() {
        return dstPort;
    }

    public void setDstPort(int dstPort) {
        this.dstPort = dstPort;
    }

    public ProtocolEnum getProtocol() {
        return protocol;
    }

    public void setProtocol(ProtocolEnum protocol) {
        this.protocol = protocol;
    }

    public String getProtocolStr() {
        switch (this.protocol.val) {
            case (6):
                return "TCP";
            case (17):
                return "UDP";
        }
        return "UNKNOWN";
    }

    public long getFlowStartTime() {
        return flowStartTime;
    }

    public void setFlowStartTime(long flowStartTime) {
        this.flowStartTime = flowStartTime;
    }

    public String getFlowId() {
        return flowId;
    }

    public void setFlowId(String flowId) {
        this.flowId = flowId;
    }

    public long getLastSeen() {
        return flowLastSeen;
    }

    public void setLastSeen(long lastSeen) {
        this.flowLastSeen = lastSeen;
    }

    public long getStartActiveTime() {
        return startActiveTime;
    }

    public void setStartActiveTime(long startActiveTime) {
        this.startActiveTime = startActiveTime;
    }

    public long getEndActiveTime() {
        return endActiveTime;
    }

    public void setEndActiveTime(long endActiveTime) {
        this.endActiveTime = endActiveTime;
    }

    public String getSrcIP() {
        return FormatUtils.ip(src);
    }

    public String getDstIP() {
        return FormatUtils.ip(dst);
    }

    public String getTimeStamp() {
        return DateFormatter.parseDateFromLong(flowStartTime / 1000L, "dd/MM/yyyy hh:mm:ss");
    }

    public long getFlowDuration() {
        return flowLastSeen - flowStartTime;
    }

    public long getTotalFwdPackets() {
        return fwdPktStats.getN();
    }

    public long getTotalBackwardPackets() {
        return bwdPktStats.getN();
    }

    public double getTotalLengthofFwdPackets() {
        return fwdPktStats.getSum();
    }

    public double getTotalLengthofBwdPackets() {
        return bwdPktStats.getSum();
    }

    public double getFwdPacketLengthMax() {
        return (fwdPktStats.getN() > 0L) ? fwdPktStats.getMax() : 0;
    }

    public double getFwdPacketLengthMin() {
        return (fwdPktStats.getN() > 0L) ? fwdPktStats.getMin() : 0;
    }

    public double getFwdPacketLengthMean() {
        return (fwdPktStats.getN() > 0L) ? fwdPktStats.getMean() : 0;
    }

    public double getFwdPacketLengthStd() {
        return (fwdPktStats.getN() > 0L) ? fwdPktStats.getStandardDeviation() : 0;
    }

    public double getBwdPacketLengthMax() {
        return (bwdPktStats.getN() > 0L) ? bwdPktStats.getMax() : 0;
    }

    public double getBwdPacketLengthMin() {
        return (bwdPktStats.getN() > 0L) ? bwdPktStats.getMin() : 0;
    }

    public double getBwdPacketLengthMean() {
        return (bwdPktStats.getN() > 0L) ? bwdPktStats.getMean() : 0;
    }

    public double getBwdPacketLengthStd() {
        return (bwdPktStats.getN() > 0L) ? bwdPktStats.getStandardDeviation() : 0;
    }

    public double getFlowBytesPerSec() {
        //flow duration is in microseconds, therefore packets per seconds = packets / (duration/1000000)
        return ((double) (forwardBytes + backwardBytes)) / ((double) getFlowDuration() / 1000000L);
    }

    public double getFlowPacketsPerSec() {
        return ((double) packetCount()) / ((double) getFlowDuration() / 1000000L);
    }

    public SummaryStatistics getFlowIAT() {
        return flowIAT;
    }

    public double getFwdIATTotal() {
        return (forward.size() > 1) ? forwardIAT.getSum() : 0;
    }

    public double getFwdIATMean() {
        return (forward.size() > 1) ? forwardIAT.getMean() : 0;
    }

    public double getFwdIATStd() {
        return (forward.size() > 1) ? forwardIAT.getStandardDeviation() : 0;
    }

    public double getFwdIATMax() {
        return (forward.size() > 1) ? forwardIAT.getMax() : 0;
    }

    public double getFwdIATMin() {
        return (forward.size() > 1) ? forwardIAT.getMin() : 0;
    }

    public double getBwdIATTotal() {
        return (backward.size() > 1) ? backwardIAT.getSum() : 0;
    }

    public double getBwdIATMean() {
        return (backward.size() > 1) ? backwardIAT.getMean() : 0;
    }

    public double getBwdIATStd() {
        return (backward.size() > 1) ? backwardIAT.getStandardDeviation() : 0;
    }

    public double getBwdIATMax() {
        return (backward.size() > 1) ? backwardIAT.getMax() : 0;
    }

    public double getBwdIATMin() {
        return (backward.size() > 1) ? backwardIAT.getMin() : 0;
    }

    public int getFwdPSHFlags() {
        return fPSH_cnt;
    }

    public int getBwdPSHFlags() {
        return bPSH_cnt;
    }

    public int getFwdURGFlags() {
        return fURG_cnt;
    }

    public int getBwdURGFlags() {
        return bURG_cnt;
    }

    public int getFwdFINFlags() {
        return fFIN_cnt;
    }

    public int getBwdFINFlags() {
        return bFIN_cnt;
    }

    public long getFwdHeaderLength() {
        return fHeaderBytes;
    }

    public long getBwdHeaderLength() {
        return bHeaderBytes;
    }

    public double getMinPacketLength() {
        return (forward.size() > 0 || backward.size() > 0) ? flowLengthStats.getMin() : 0;
    }

    public double getMaxPacketLength() {
        return (forward.size() > 0 || backward.size() > 0) ? flowLengthStats.getMax() : 0;
    }

    public double getPacketLengthMean() {
        return (forward.size() > 0 || backward.size() > 0) ? flowLengthStats.getMean() : 0;
    }

    public double getPacketLengthStd() {
        return (forward.size() > 0 || backward.size() > 0) ? flowLengthStats.getStandardDeviation() : 0;
    }

    public double getPacketLengthVariance() {
        return (forward.size() > 0 || backward.size() > 0) ? flowLengthStats.getVariance() : 0;
    }

    public int getFlagCount(String key) {
        return flagCounts.get(key).value;
    }

    public int getInit_Win_bytes_forward() {
        return Init_Win_bytes_forward;
    }

    public int getInit_Win_bytes_backward() {
        return Init_Win_bytes_backward;
    }

    public long getAct_data_pkt_forward() {
        return Act_data_pkt_forward;
    }

    public long getAct_data_pkt_backward() {
        return Act_data_pkt_backward;
    }

    public long getmin_seg_size_forward() {
        return min_seg_size_forward;
    }

    public long getmin_seg_size_backward() {
        return min_seg_size_backward;
    }

    public double getActiveMean() {
        return (flowActive.getN() > 0) ? flowActive.getMean() : 0;
    }

    public double getActiveStd() {
        return (flowActive.getN() > 0) ? flowActive.getStandardDeviation() : 0;
    }

    public double getActiveMax() {
        return (flowActive.getN() > 0) ? flowActive.getMax() : 0;
    }

    public double getActiveMin() {
        return (flowActive.getN() > 0) ? flowActive.getMin() : 0;
    }

    public double getIdleMean() {
        return (flowIdle.getN() > 0) ? flowIdle.getMean() : 0;
    }

    public double getIdleStd() {
        return (flowIdle.getN() > 0) ? flowIdle.getStandardDeviation() : 0;
    }

    public double getIdleMax() {
        return (flowIdle.getN() > 0) ? flowIdle.getMax() : 0;
    }

    public double getIdleMin() {
        return (flowIdle.getN() > 0) ? flowIdle.getMin() : 0;
    }

    public String getCaptureInerface() {
        return captureInterface;
    }

    public String getCaptureHost() {
        return captureHost;
    }
    public TcpFlowState getTcpFlowState() {
        return this.tcpFlowState;
    }

    public void setTcpFlowState(TcpFlowState state) {
        this.tcpFlowState = state;
    }

    public long getCumulativeConnectionDuration() {
        return this.cumulativeConnectionDuration;
    }

    public void setCumulativeConnectionDuration(long cumCnxDuration) {
        this.cumulativeConnectionDuration = cumCnxDuration;
    }

    public Set<TcpRetransmissionDTO> getTcpPacketsSeen() {
        return this.tcpPacketsSeen;
    }

    public void setTcpPacketsSeen(Set<TcpRetransmissionDTO> tcpPacketsSeen) {
        this.tcpPacketsSeen = tcpPacketsSeen;
    }

    public int getIcmpCode() {
        return this.icmpCode;
    }

    public int getIcmpType() {
        return this.icmpType;
    }


    public String getLabel() {
        //the original is "|". I think it should be "||" need to check,
		/*if(FormatUtils.ip(src).equals("147.32.84.165") || FormatUtils.ip(dst).equals("147.32.84.165")){
			return "BOTNET";
		}
		else{
			return "BENIGN";
		}*/
        return "NeedManualLabel";
    }

    public String dumpFlowBasedFeaturesEx() {
        StringBuilder dump = new StringBuilder();

        dump.append(flowId).append(separator);                                        //1
        dump.append(FormatUtils.ip(src)).append(separator);                        //2
        dump.append(getSrcPort()).append(separator);                                //3
        dump.append(FormatUtils.ip(dst)).append(separator);                        //4
        dump.append(getDstPort()).append(separator);                                //5
        dump.append(getProtocol().val).append(separator);                                //6

        String starttime = DateFormatter.convertEpochTimestamp2String(flowStartTime);
        dump.append(starttime).append(separator);                                    //7

        long flowDuration = flowLastSeen - flowStartTime;
        dump.append(flowDuration).append(separator);                                //8

        dump.append(fwdPktStats.getN()).append(separator);                            //9
        dump.append(bwdPktStats.getN()).append(separator);                            //10
        dump.append(fwdPktStats.getSum()).append(separator);                        //11
        dump.append(bwdPktStats.getSum()).append(separator);                        //12

        if (fwdPktStats.getN() > 0L) {
            dump.append(fwdPktStats.getMax()).append(separator);                    //13
            dump.append(fwdPktStats.getMin()).append(separator);                    //14
            dump.append(fwdPktStats.getMean()).append(separator);                    //15
            dump.append(fwdPktStats.getStandardDeviation()).append(separator);        //16
        } else {
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }

        if (bwdPktStats.getN() > 0L) {
            dump.append(bwdPktStats.getMax()).append(separator);                    //17
            dump.append(bwdPktStats.getMin()).append(separator);                    //18
            dump.append(bwdPktStats.getMean()).append(separator);                    //19
            dump.append(bwdPktStats.getStandardDeviation()).append(separator);        //20
        } else {
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }

        if(flowDuration != 0){
            dump.append(((double) (forwardBytes + backwardBytes)) / ((double) flowDuration / 1000000L)).append(separator); //21
            dump.append(((double) packetCount()) / ((double) flowDuration / 1000000L)).append(separator); // 22
        }else{
            dump.append(-1).append(separator);
            dump.append(-1).append(separator);
        }

        dump.append(Double.isNaN(flowIAT.getMean()) ? 0 : flowIAT.getMean()).append(separator);  // 23
        dump.append(Double.isNaN(flowIAT.getStandardDeviation()) ? 0 : flowIAT.getStandardDeviation()).append(separator); //24
        dump.append(Double.isNaN(flowIAT.getMax()) ? 0 : flowIAT.getMax()).append(separator);    //25
        dump.append(Double.isNaN(flowIAT.getMin()) ? 0 : flowIAT.getMin()).append(separator);                         //26

        if (this.forward.size() > 1) {
            dump.append(forwardIAT.getSum()).append(separator);                        //27
            dump.append(forwardIAT.getMean()).append(separator);                    //28
            dump.append(forwardIAT.getStandardDeviation()).append(separator);        //29
            dump.append(forwardIAT.getMax()).append(separator);                        //30
            dump.append(forwardIAT.getMin()).append(separator);                        //31

        } else {
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }
        if (this.backward.size() > 1) {
            dump.append(backwardIAT.getSum()).append(separator);                    //32
            dump.append(backwardIAT.getMean()).append(separator);                    //33
            dump.append(backwardIAT.getStandardDeviation()).append(separator);        //34
            dump.append(backwardIAT.getMax()).append(separator);                    //35
            dump.append(backwardIAT.getMin()).append(separator);                    //36
        } else {
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }

        dump.append(fPSH_cnt).append(separator);                                    //37
        dump.append(bPSH_cnt).append(separator);                                    //38
        dump.append(fURG_cnt).append(separator);                                    //39
        dump.append(bURG_cnt).append(separator);                                    //40
        dump.append(fRST_cnt).append(separator);                                    //41
        dump.append(bRST_cnt).append(separator);                                    //42

        dump.append(fHeaderBytes).append(separator);                                //43
        dump.append(bHeaderBytes).append(separator);                                //44
        dump.append(getfPktsPerSecond()).append(separator);                            //45
        dump.append(getbPktsPerSecond()).append(separator);                            //46


        if (this.forward.size() > 0 || this.backward.size() > 0) {
            dump.append(flowLengthStats.getMin()).append(separator);                //47
            dump.append(flowLengthStats.getMax()).append(separator);                //48
            dump.append(flowLengthStats.getMean()).append(separator);                //49
            dump.append(flowLengthStats.getStandardDeviation()).append(separator);    //50
            dump.append(flowLengthStats.getVariance()).append(separator);            //51
        } else {//seem to less one
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }

		/*for(MutableInt v:flagCounts.values()) {
			dump.append(v).append(separator);
		}
		for(String key: flagCounts.keySet()){
			dump.append(flagCounts.get(key).value).append(separator);				//50,51,52,53,54,55,56,57
		} */
        dump.append(flagCounts.get("FIN").value).append(separator);                 //52
        dump.append(flagCounts.get("SYN").value).append(separator);                 //53
        dump.append(flagCounts.get("RST").value).append(separator);                  //54
        dump.append(flagCounts.get("PSH").value).append(separator);                  //55
        dump.append(flagCounts.get("ACK").value).append(separator);                  //56
        dump.append(flagCounts.get("URG").value).append(separator);                  //57
        dump.append(flagCounts.get("CWR").value).append(separator);                  //58
        dump.append(flagCounts.get("ECE").value).append(separator);                  //59

        dump.append(getDownUpRatio()).append(separator);                            //60
        dump.append(getAvgPacketSize()).append(separator);                            //61
        dump.append(fAvgSegmentSize()).append(separator);                            //62
        dump.append(bAvgSegmentSize()).append(separator);                            //63
        //dump.append(fHeaderBytes).append(separator);								//62 dupicate with 43

        dump.append(fAvgBytesPerBulk()).append(separator);                            //64
        dump.append(fAvgPacketsPerBulk()).append(separator);                        //65
        dump.append(fAvgBulkRate()).append(separator);                                //66
        dump.append(bAvgBytesPerBulk()).append(separator);                            //67
        dump.append(bAvgPacketsPerBulk()).append(separator);                        //68
        dump.append(bAvgBulkRate()).append(separator);                                //69

        dump.append(getSflow_fpackets()).append(separator);                            //70
        dump.append(getSflow_fbytes()).append(separator);                            //71
        dump.append(getSflow_bpackets()).append(separator);                            //72
        dump.append(getSflow_bbytes()).append(separator);                            //73

        dump.append(Init_Win_bytes_forward).append(separator);                        //74
        dump.append(Init_Win_bytes_backward).append(separator);                        //75
        dump.append(Act_data_pkt_forward).append(separator);                            //76
        dump.append(Act_data_pkt_backward).append(separator);                           //77
        dump.append(min_seg_size_forward).append(separator);                        //78
        dump.append(min_seg_size_backward).append(separator);                       //79


        if (this.flowActive.getN() > 0) {
            dump.append(flowActive.getMean()).append(separator);                    //80
            dump.append(flowActive.getStandardDeviation()).append(separator);        //81
            dump.append(flowActive.getMax()).append(separator);                        //82
            dump.append(flowActive.getMin()).append(separator);                        //83
        } else {
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }

        if (this.flowIdle.getN() > 0) {
            dump.append(flowIdle.getMean()).append(separator);                        //84
            dump.append(flowIdle.getStandardDeviation()).append(separator);            //85
            dump.append(flowIdle.getMax()).append(separator);                        //86
            dump.append(flowIdle.getMin()).append(separator);                        //87
        } else {
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
            dump.append(0).append(separator);
        }

        dump.append(icmpCode).append(separator);                                    // 88
        dump.append(icmpType).append(separator);                                    // 89

        dump.append(fwdTcpRetransCnt).append(separator);                                    // 88
        dump.append(bwdTcpRetransCnt).append(separator);                                    // 89
        dump.append(fwdTcpRetransCnt+bwdTcpRetransCnt).append(separator);                   // 90

        dump.append(cumulativeConnectionDuration).append(separator);                //91
        dump.append(getLabel());                                                    //92

        return dump.toString();
    }

    public ObjectNode dumpJsonFlowBasedFeaturesEx() {
        ObjectMapper mapper = jacksonObjectMapper();
        ObjectNode features = mapper.createObjectNode();

        features.put("flow_id", flowId);
        features.put("ip_src", FormatUtils.ip(src));
        features.put("ip_src_prt", getSrcPort());
        features.put("ip_dst", FormatUtils.ip(dst));
        features.put("ip_dst_prt", getDstPort());
        features.put("protocol", getProtocol().val);

        String starttime = DateFormatter.convertEpochTimestamp2String(flowStartTime);
        features.put("timestamp", starttime);//7

        long flowDuration = flowLastSeen - flowStartTime;
        features.put("flow_duration", flowDuration);

        features.put("fwd_pkt_stats", fwdPktStats.getN());
        features.put("bwd_pkt_stats", bwdPktStats.getN());
        features.put("tot_l_fw_pkt", fwdPktStats.getSum());
        features.put("tot_l_bw_pkt", bwdPktStats.getSum());

        if (fwdPktStats.getN() > 0L) {
            features.put("fw_pkt_l_max", fwdPktStats.getMax());
            features.put("fw_pkt_l_min", fwdPktStats.getMin());
            features.put("fw_pkt_l_avg", fwdPktStats.getMean());
            features.put("fw_pkt_l_std", fwdPktStats.getStandardDeviation());
        } else {
            features.put("fw_pkt_l_max", 0);
            features.put("fw_pkt_l_min", 0);
            features.put("fw_pkt_l_avg", 0);
            features.put("fw_pkt_l_std", 0);
        }

        if (this.backward.size() > 1) {
            features.put("bw_iat_tot", backwardIAT.getSum());
            features.put("bw_iat_avg", backwardIAT.getMean());
            features.put("bw_iat_std", backwardIAT.getStandardDeviation());
            features.put("bw_iat_max", backwardIAT.getMax());
            features.put("bw_iat_min", backwardIAT.getMin());
        } else {
            features.put("bw_iat_tot", 0);
            features.put("bw_iat_avg", 0);
            features.put("bw_iat_std", 0);
            features.put("bw_iat_max", 0);
            features.put("bw_iat_min", 0);
        }

        features.put("fw_psh_flag", fPSH_cnt);
        features.put("bw_psh_flag", bPSH_cnt);
        features.put("fw_urg_flag", fURG_cnt);
        features.put("bw_urg_flag", bURG_cnt);
        features.put("fw_rst_flag", fRST_cnt);
        features.put("bw_rst_flag", bRST_cnt);

        features.put("fw_hdr_len", fHeaderBytes);
        features.put("bw_hdr_len", bHeaderBytes);
        features.put("fw_pkt_s", getfPktsPerSecond());
        features.put("bw_pkt_s", getbPktsPerSecond());

        if (this.forward.size() > 0 || this.backward.size() > 0) {
            features.put("pkt_len_min", flowLengthStats.getMin());
            features.put("pkt_len_max", flowLengthStats.getMax());
            features.put("pkt_len_avg", flowLengthStats.getMean());
            features.put("pkt_len_std", flowLengthStats.getStandardDeviation());
            features.put("pkt_len_va", flowLengthStats.getVariance());
        } else {
            features.put("pkt_len_min", 0);
            features.put("pkt_len_max", 0);
            features.put("pkt_len_avg", 0);
            features.put("pkt_len_std", 0);
            features.put("pkt_len_va", 0);
        }

        features.put("fin_cnt", flagCounts.get("FIN").value);
        features.put("syn_cnt", flagCounts.get("SYN").value);
        features.put("rst_cnt", flagCounts.get("RST").value);
        features.put("pst_cnt", flagCounts.get("PSH").value);
        features.put("ack_cnt", flagCounts.get("ACK").value);
        features.put("urg_cnt", flagCounts.get("URG").value);
        features.put("cwe_cnt", flagCounts.get("CWR").value);
        features.put("ece_cnt", flagCounts.get("ECE").value);

        features.put("down_up_ratio", getDownUpRatio());
        features.put("pkt_size_avg", getAvgPacketSize());
        features.put("fw_seg_avg", fAvgSegmentSize());
        features.put("bw_seg_avg", bAvgSegmentSize());

        features.put("fw_byt_blk_avg", fAvgBytesPerBulk());
        features.put("fw_pkt_blk_avg", fAvgPacketsPerBulk());
        features.put("fw_blk_rate_avg", fAvgBulkRate());
        features.put("bw_byt_blk_avg", bAvgBytesPerBulk());
        features.put("bw_pkt_blk_avg", bAvgPacketsPerBulk());
        features.put("bw_blk_rate_avg", bAvgBulkRate());

        features.put("subfl_fw_pk", getSflow_fpackets());
        features.put("subfl_fw_byt", getSflow_fbytes());
        features.put("subfl_bw_pkt", getSflow_bpackets());
        features.put("subfl_bw_byt", getSflow_bbytes());

        features.put("fw_win_byt", Init_Win_bytes_forward);
        features.put("bw_win_byt", Init_Win_bytes_backward);
        features.put("Fw_act_pkt", Act_data_pkt_forward);
        features.put("fw_seg_min", min_seg_size_forward);

// Note: Act_data_pkt_backward and min_seg_size_backward are not in the feature list you provided earlier
        features.put("Bw_act_pkt", Act_data_pkt_backward);
        features.put("bw_seg_min", min_seg_size_backward);

        if (this.flowActive.getN() > 0) {
            features.put("atv_avg", flowActive.getMean());
            features.put("atv_std", flowActive.getStandardDeviation());
            features.put("atv_max", flowActive.getMax());
            features.put("atv_min", flowActive.getMin());
        } else {
            features.put("atv_avg", 0);
            features.put("atv_std", 0);
            features.put("atv_max", 0);
            features.put("atv_min", 0);
        }

        if (this.flowIdle.getN() > 0) {
            features.put("idl_avg", flowIdle.getMean());
            features.put("idl_std", flowIdle.getStandardDeviation());
            features.put("idl_max", flowIdle.getMax());
            features.put("idl_min", flowIdle.getMin());
        } else {
            features.put("idl_avg", 0);
            features.put("idl_std", 0);
            features.put("idl_max", 0);
            features.put("idl_min", 0);
        }

        features.put("icmp_code", icmpCode);
        features.put("icmp_type", icmpType);

        features.put("fwd_tcp_retrans_cnt", fwdTcpRetransCnt);
        features.put("bwd_tcp_retrans_cnt", bwdTcpRetransCnt);
        features.put("total_tcp_retrans_cnt", fwdTcpRetransCnt + bwdTcpRetransCnt);

        features.put("cumulative_connection_duration", cumulativeConnectionDuration);
        features.put("label", getLabel());

        return features;
    }
}

class MutableInt {
    int value = 0; // note that we start at 1 since we're counting

    public void increment() {
        ++value;
    }

    public int get() {
        return value;
    }


}
