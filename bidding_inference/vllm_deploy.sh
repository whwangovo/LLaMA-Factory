# API_PORT=8000 llamafactory-cli api bidding_srcipts/bidding_inference.yaml
vllm serve bidding_outputs/finetune_outputs/bidding_pretrain_finetune_250227 --served-model-name qwen_chat --port 8000