#!/bin/bash
# Generate python code from proto file
for proto in voicebot.proto streaming_voice.proto chatbot.proto; do
    if [ ! -f protos/$proto ]; then
        echo "Error! Not found protos/$proto!"
        exit 1
    fi
    echo "python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/$proto"
    python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/$proto
done
echo "Done!"
