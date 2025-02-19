package com.vanwaasen.cicfm.flink;

import cic.cs.unb.ca.jnetpcap.BasicPacketInfo;
import cic.cs.unb.ca.jnetpcap.FlowGenerator;
import com.vanwaasen.cicfm.PacketProcessor;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class KafkaFlinkProcessor {

    private static final Logger LOG = LoggerFactory.getLogger(KafkaFlinkProcessor.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) throws Exception {

        final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(5000);

        String configFilePath = "/opt/flink/usrlib/kafka-config.properties";
        ParameterTool parameters = ParameterTool.fromPropertiesFile(configFilePath);

        String bootstrapSourceServers = parameters.get("kafka.bootstrap.source.servers", null);
        String bootstrapSinkServers = parameters.get("kafka.bootstrap.sink.servers", null);
        String sourceTopic = parameters.get("kafka.source.topic", null);
        String sinkTopic = parameters.get("kafka.sink.topic", null);
        String groupId = parameters.get("kafka.group.id", null);

        KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                .setBootstrapServers(bootstrapSourceServers)
                .setTopics(sourceTopic)
                .setGroupId(groupId)
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        LOG.info("Attempting to subscribe to Kafka topic: packet-features with group ID: flink-consumer-group");

        DataStream<String> stream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "Kafka Source");

        LOG.info("Successfully subscribed to Kafka topic: packet-features");

        DataStream<String> flowStream = stream
                .keyBy(message -> {
                    try {
                        JsonNode jsonNode = objectMapper.readTree(message);
                        String captureHost = jsonNode.has("capture_host") ? jsonNode.get("capture_host").asText() : "unknown";
                        String captureInterface = jsonNode.has("capture_interface_name") ? jsonNode.get("capture_interface_name").asText() : "unknown";
                        return captureHost + ":" + captureInterface;
                    } catch (Exception e) {
                        LOG.error("🚨 JSON parsing failed! {} Raw Message: {}", message, e.getMessage());
                        return "unknown:unknown"; // Handle errors gracefully
                    }
                })
                .process(new FlowProcessor());

        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("max.request.size", "10485760");

        KafkaSink<String> kafkaSink = KafkaSink.<String>builder()
                .setBootstrapServers(bootstrapSinkServers)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(sinkTopic)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build())
                        .setKafkaProducerConfig(kafkaProps)
                .build();

        flowStream.sinkTo(kafkaSink);

        env.execute("63184 Flink Kafka Processor");
    }

    public static class FlowProcessor extends KeyedProcessFunction<String, String, String> {

        private static final long FLOW_TIMEOUT = 120000; // 2 minutes in milliseconds
        private ValueState<String> flowState;

        private FlowGenerator flowGen;
        private FlinkFlowListener flinkFlowListener;
        private Queue<String> flowQueue;
        private PacketProcessor packetProcessor;

        private long nValid = 0;
        private long nTotal = 0;
        private long nDiscarded = 0;
        private long i = 0;

        @Override
        public void open(Configuration parameters) throws Exception {
            super.open(parameters);

            // Load configuration from Flink's Configuration object
            Map<String, Object> configMap = new HashMap<>();
            parameters.toMap().forEach((key, value) -> configMap.put(key, value));

            long flowTimeout = 120000000L;
            long activityTimeout = 5000000L;
            boolean readIP6 = false;
            boolean readIP4 = true;

            flowQueue = new ConcurrentLinkedQueue<>();

            flowGen = new FlowGenerator(true, flowTimeout, activityTimeout);
            flinkFlowListener = new FlinkFlowListener(flowQueue);
            flowGen.addFlowListener(flinkFlowListener);
            packetProcessor = new PacketProcessor();
        }

        @Override
        public void processElement(String jsonValue, Context ctx, Collector<String> out) throws Exception {

            try {
                JsonNode jsonNode = objectMapper.readTree(jsonValue);

                BasicPacketInfo basicPacket = null;
                JsonNode ipVersionNode = jsonNode.path("_source")
                        .path("layers")
                        .path("ip")
                        .path("ip_ip_version");

                int ipVersion = ipVersionNode.asInt();
                if (ipVersion == 4) {
                    basicPacket = packetProcessor.getIpv4Info(jsonNode);
                }

                nTotal++;

                if (basicPacket != null) {

                    flowGen.addPacket(basicPacket, jsonValue);
                    nValid++;
                } else {
                    nDiscarded++;
                }
                i++;
            }catch(Exception e) {
                LOG.error("🚨 JSON parsing failed! {} Raw Message: {}", ctx.getCurrentKey(), e.getMessage());

            }finally {
                while (!flowQueue.isEmpty()) {
                    String flowMessage = flowQueue.poll(); // Retrieve and remove one message from the queue
                    if (flowMessage != null) {
                        out.collect(flowMessage); // Emit each message downstream
                    }
                }
            }
        }
    }
}
