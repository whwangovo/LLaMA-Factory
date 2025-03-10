# API_PORT=8000 llamafactory-cli api bidding_srcipts/bidding_inference.yaml
vllm serve checkpoints/Qwen/Qwen2.5-32B-Instruct --tensor-parallel-size 2 \
                                                 --max-model-len 16384 \
                                                 --enable-lora \
                                                 --lora-modules rw=bidding_outputs/finetune_outputs/finetune@32B@lora@pure@FGIRCS@20250310 \
                                                 # cs=bidding_outputs/finetune_outputs/finetune@lora@continue_summary@250228