# API_PORT=8000 llamafactory-cli api bidding_srcipts/bidding_inference.yaml
vllm serve bidding_outputs/finetune_outputs/finetune@pt@FGIRCS@20250306 \
                                                 --tensor-parallel-size 8 \
                                                 --served-model-name qwen_chat \
                                                 --port 8000