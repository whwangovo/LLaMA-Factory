
vllm serve checkpoints/Qwen/Qwen2.5-14B-Instruct \
                                                 --tensor-parallel-size 1 \
                                                 --served-model-name qwen_chat \
                                                 --port 8000