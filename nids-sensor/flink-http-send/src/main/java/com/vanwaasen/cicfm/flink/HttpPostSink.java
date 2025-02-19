package com.vanwaasen.cicfm.flink;

import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.connector.sink2.SinkWriter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.*;

public class HttpPostSink implements Sink<String> {

    private final String endpointUrl;
    private final String serverKey;

    public HttpPostSink(String endpointUrl, String serverKey) {
        this.endpointUrl = endpointUrl;
        this.serverKey = serverKey;
    }

    @Override
    public SinkWriter<String> createWriter(Sink.InitContext initContext) {  // ✅ Fix: Correct Flink method
        return new HttpPostWriter(endpointUrl, serverKey);
    }

    public static class HttpPostWriter implements SinkWriter<String> {
        private static final Logger LOG = LoggerFactory.getLogger(HttpPostWriter.class);

        private final String endpointUrl;
        private final String serverKey;
        private final ExecutorService executorService;
        private final CompletionService<Boolean> completionService;
        private static final int MAX_PENDING_REQUESTS = 100;

        public HttpPostWriter(String endpointUrl, String serverKey) {
            this.endpointUrl = endpointUrl;
            this.serverKey = serverKey;
            this.executorService = Executors.newFixedThreadPool(10);
            this.completionService = new ExecutorCompletionService<>(executorService);
        }

        @Override
        public void write(String record, Context context) {
            completionService.submit(() -> {
                try {
                    URL url = new URL(endpointUrl);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json");
                    conn.setRequestProperty("Authorization", "Bearer " + serverKey);
                    conn.setDoOutput(true);

                    try (OutputStream os = conn.getOutputStream()) {
                        byte[] input = record.getBytes(StandardCharsets.UTF_8);
                        os.write(input, 0, input.length);
                    }

                    int responseCode = conn.getResponseCode();
                    LOG.info("📩 HTTP POST Response Code: {}", responseCode);
                    return responseCode == 200;
                } catch (Exception e) {
                    LOG.error("❌ Error sending HTTP request", e);
                    return false;
                }
            });

            while (((ThreadPoolExecutor) executorService).getQueue().size() > MAX_PENDING_REQUESTS) {
                try {
                    completionService.take().get();
                } catch (Exception e) {
                    LOG.error("❌ Error waiting for HTTP request completion", e);
                }
            }
        }

        @Override
        public void flush(boolean endOfInput) {
            LOG.info("🔄 Flushing HTTP requests...");

            while (((ThreadPoolExecutor) executorService).getActiveCount() > 0) {
                try {
                    Future<Boolean> future = completionService.take();
                    future.get();
                } catch (Exception e) {
                    LOG.error("❌ Error during flush", e);
                }
            }

            LOG.info("✅ HTTP Sink flush completed.");
        }

        @Override
        public void close() {
            flush(true);
            LOG.info("✅ Closing HTTP Sink...");
            executorService.shutdown();

            try {
                if (!executorService.awaitTermination(10, TimeUnit.SECONDS)) {
                    LOG.warn("⚠️ HTTP Sink executor did not terminate in time!");
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                LOG.error("❌ Interrupted while shutting down HTTP Sink", e);
            }

            LOG.info("✅ HTTP Sink closed successfully.");
        }
    }
}
