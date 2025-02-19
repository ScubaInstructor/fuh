package com.vanwaasen.cicfm.flink;


import cic.cs.unb.ca.jnetpcap.BasicFlow;
import cic.cs.unb.ca.jnetpcap.BasicPacketInfo;
import cic.cs.unb.ca.jnetpcap.FlowFeature;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.vanwaasen.cicfm.CICFlowListener;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Queue;

public class FlinkFlowListener implements CICFlowListener {

    private final ObjectMapper mapper = new ObjectMapper();
    private final DateTimeFormatter dateFormatter
            = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    private final Queue<String> flowQueue;
    String[] theHeader = null;

    public FlinkFlowListener(Queue<String> flowQueue) {
        this.flowQueue = flowQueue;

        String flowHeader = FlowFeature.getHeader();
        String[] headerArray = flowHeader.split(",");

        theHeader = new String[headerArray.length];
        for (int i = 0; i < headerArray.length; i++) {
            theHeader[i] = headerArray[i].toLowerCase().replaceAll("[^a-z0-9]", "_");
        }
    }

    public void onFlowGenerated(BasicFlow flow) {
        try {
            String flowDump = flow.dumpFlowBasedFeaturesEx();
            ObjectNode theFlowFeatures = JsonFlowData.convertToJson(theHeader, flowDump);

            LocalDate currentDate = LocalDate.now();
            String formattedDate = currentDate.format(dateFormatter);

            ObjectNode elasticJson = mapper.createObjectNode();
            elasticJson.put("_index", "flow-" + formattedDate);
            elasticJson.put("_type", "doc");
            elasticJson.putNull("_score");

            ObjectNode sourceNode = elasticJson.putObject("_source");
            sourceNode.put("capture_host", flow.getCaptureHost());
            sourceNode.put("capture_interface", flow.getCaptureInerface());
            sourceNode.put("flow_id", flow.getFlowId());
            sourceNode.put("features_ex", flowDump);
            sourceNode.set("flowFeatures", theFlowFeatures);

            ArrayNode forwardPacketsNode = mapper.createArrayNode();
            for (BasicPacketInfo packet : flow.getForward()) {
                JsonNode packetJson = null;
                try {
                    packetJson = mapper.readTree(packet.getJsonRepresentation());
                } catch (JsonProcessingException e) {
                    throw new RuntimeException(e);
                }
                JsonNode sourcePacketNode = packetJson.get("_source");

                if (sourcePacketNode instanceof ObjectNode) {
                    ((ObjectNode) sourcePacketNode).put("flow_id", flow.getFlowId());
                    ((ObjectNode) sourcePacketNode).put("direction", "forward");
                }
                forwardPacketsNode.add(packetJson);
            }
            sourceNode.set("forwardPackets", forwardPacketsNode);

            ArrayNode backwardPacketsNode = mapper.createArrayNode();
            for (BasicPacketInfo packet : flow.getBackward()) {
                JsonNode packetJson = mapper.readTree(packet.getJsonRepresentation());
                JsonNode sourcePacketNode = packetJson.get("_source");

                if (sourcePacketNode instanceof ObjectNode) {
                    ((ObjectNode) sourcePacketNode).put("flow_id", flow.getFlowId());
                    ((ObjectNode) sourcePacketNode).put("direction", "backward");
                }
                backwardPacketsNode.add(packetJson);
            }
            sourceNode.set("backwardPackets", backwardPacketsNode);

            String compactJson = mapper.writeValueAsString(elasticJson);
            boolean offered = flowQueue.offer(compactJson);
            if (!offered) {
                System.err.println("Failed to add flow to queue!");
            }
        } catch (Exception e) {
            throw new RuntimeException("Error generating flow JSON", e);
        }
    }
}