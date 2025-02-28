VLLM_WORKER_MULTIPROC_METHOD=spawn vllm serve checkpoints/DeepSeek-R1-awq --host 0.0.0.0 --port 12345 \
                                               --max-model-len 65536 --max-num-batched-tokens 65536 \
                                               --trust-remote-code --tensor-parallel-size 8 --gpu-memory-utilization 0.97 \
                                               --dtype float16 --served-model-name deepseek-reasoner \
