# API_PORT=8000 llamafactory-cli api bidding_srcipts/bidding_inference.yaml
vllm serve checkpoints/Qwen/Qwen2.5-32B-Instruct \
                                                 --tensor-parallel-size 8 \
                                                 --served-model-name qwen_chat \
                                                 --port 8000