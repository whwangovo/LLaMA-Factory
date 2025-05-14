# API_PORT=8000 llamafactory-cli api bidding_srcipts/bidding_inference.yaml
CUDA_VISIBLE_DEVICES=6,7 vllm serve /home/lt_08321/ssd/wangweihang/LLaMA-Factory/bidding_outputs/finetune_outputs/sft@14B@pt@full@Wrting@250415 --served-model-name qwen_chat --port 8001
CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve /home/lt_08321/ssd/wangweihang/LLaMA-Factory/checkpoints/Qwen/Qwen2.5-14B-Instruct --served-model-name qwen_chat_14 --port 8001
CUDA_VISIBLE_DEVICES=4,5,6,7 vllm serve /home/lt_08321/ssd/wangweihang/LLaMA-Factory/checkpoints/Qwen/Qwen2.5-32B-Instruct --served-model-name qwen_chat_32 --port 8002
vllm serve /home/lt_08321/ssd/wangweihang/LLaMA-Factory/bidding_outputs/finetune_outputs/sft@14B@pt@full@gkx@250505 --served-model-name qwen_chat_14 --port 8001