# API_PORT=8000 llamafactory-cli api bidding_srcipts/bidding_inference.yaml
vllm serve bidding_outputs/finetune_outputs/sft@14B@pt@full@Wrting@250415 \
                                                 --tensor-parallel-size 1 \
                                                 --max-model-len 16384 \
                                                 --served-model-name qwen_chat \
                                                 --port 8001 \
                                                 --gpu_memory_utilizatio 0.98