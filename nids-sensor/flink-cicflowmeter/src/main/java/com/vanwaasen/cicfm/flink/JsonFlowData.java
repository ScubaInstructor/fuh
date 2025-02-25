package com.vanwaasen.cicfm.flink;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class JsonFlowData {

    public static ObjectNode convertToJson(String[] headers, String values) throws Exception {
        String[] valueArray = values.split(",");

        if (headers.length != valueArray.length) {
            throw new IllegalArgumentException("Headers and values have different lengths");
        }

        ObjectMapper objectMapper = new ObjectMapper();
        ObjectNode jsonNode = objectMapper.createObjectNode();

        for (int i = 0; i < headers.length; i++) {
            String key = headers[i];
            String value = valueArray[i];

            try {
                // Try parsing as double first
                double doubleValue = Double.parseDouble(value);
                if (value.contains(".")) {
                    jsonNode.put(key, doubleValue);
                } else {
                    // If it's a whole number, store as long
                    jsonNode.put(key, (long) doubleValue);
                }
            } catch (NumberFormatException e) {
                // If parsing fails, it's a string
                jsonNode.put(key, value);
            }
        }

        return jsonNode;
    }
}
