package com.vanwaasen.cicfm.flink;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.util.*;

public class HttpFlinkProcessor {

    private static final Logger LOG = LoggerFactory.getLogger(HttpFlinkProcessor.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) throws Exception {

        final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(5000);

        String configFilePath = "/opt/flink/usrlib/http-sender-config.properties";
        ParameterTool parameters = ParameterTool.fromPropertiesFile(configFilePath);

        String bootstrapSourceServers = parameters.get("kafka.bootstrap.source.servers", null);
        String sourceTopic = parameters.get("kafka.source.topic", null);
        String groupId = parameters.get("kafka.group.id", null);
        String sensor_name = parameters.get("ids.sensor.name", "not registered yet");

        KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                .setBootstrapServers(bootstrapSourceServers)
                .setTopics(sourceTopic)
                .setGroupId(groupId)
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        DataStream<String> stream = env.fromSource(kafkaSource,
                WatermarkStrategy.noWatermarks(), "Kafka Networkflows Source");

        DataStream<String> flowStream = stream
                .process(new FlowProcessor(sensor_name));

        String httpServer = parameters.get("http.sink.server", null);
        String serverKey = parameters.get("http.sink.server.key", null);

        flowStream.sinkTo(new HttpPostSink(httpServer, serverKey));

        env.execute("63184 Flink Sender Processor");
    }

    public static class FlowProcessor extends ProcessFunction<String, String> {

        private ObjectMapper objectMapper;
        private final String sensorName;

        public FlowProcessor(String sensorName) {
            this.sensorName = sensorName;
        }

        @Override
        public void open(Configuration parameters) throws Exception {
            super.open(parameters);

            this.objectMapper = new ObjectMapper();
        }

        @Override
        public void processElement(String jsonValue, Context ctx, Collector<String> out) throws Exception {

            try {
                JsonNode jsonNode = objectMapper.readTree(jsonValue);

                ObjectNode resultJson = objectMapper.createObjectNode();
                String flowId = jsonNode.path("_source").path("flow_id").asText();
                resultJson.put("sensor_name", sensorName);
                resultJson.put("flow_id", UUID.randomUUID().toString());

                resultJson.set("flow_data",
                        jsonNode.path("_source").get("flowFeatures"));
                resultJson.set("flow_ex",
                        jsonNode.path("_source").path("features_ex"));
                resultJson.set("timestamp", jsonNode.path("_source")
                        .path("flowFeatures")
                        .path("timestamp"));
                resultJson.set("dst_ip",
                        jsonNode.path("_source").path("flowFeatures").path("ip_dst"));
                resultJson.set("dst_prt",
                        jsonNode.path("_source").path("flowFeatures").get("ip_dst_prt"));
                resultJson.set("src_ip",
                        jsonNode.path("_source").path("flowFeatures").path("ip_src"));
                resultJson.set("src_prt",
                        jsonNode.path("_source").path("flowFeatures").get("ip_src_prt"));

                List<String> pcapBinaryList = new ArrayList<>();

                // Loop over both "forwardPackets" and "backwardPackets" dynamically
                List<String> packetTypes = Arrays.asList("forwardPackets", "backwardPackets");

                for (String packetType : packetTypes) {
                    JsonNode packetsArray = jsonNode.path("_source").path(packetType);
                    if (packetsArray.isArray()) {
                        for (JsonNode packetNode : packetsArray) {
                            String pcapBinary =
                                    packetNode.path("_source").path("pcap_binary").asText();
                            if (!pcapBinary.isEmpty()) {
                                pcapBinaryList.add(pcapBinary);
                            }
                        }
                    }
                }

                if(!pcapBinaryList.isEmpty()) {

                    byte[] pcapFile = PcapMerger.mergePcapPackets(pcapBinaryList);
                    String base64Pcap = Base64.getEncoder().encodeToString(pcapFile);

                    resultJson.put("pcap_data", base64Pcap);
                }else{
                    resultJson.put("pcap_data", "NO pcap data!!");
                }


                String compactJson = resultJson.toString();

                out.collect(compactJson);

            } catch (Exception e) {
                LOG.error("Error processing JSON flow: {}", jsonValue, e);
            }
        }
    }

}
