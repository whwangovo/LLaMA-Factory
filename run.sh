#!/bin/bash
# CUDA_VISIBLE_DEVICES=0,1 llamafactory-cli train examples/train_full/qwen25_full_sft.yaml
CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7 llamafactory-cli train /home/lt_08321/ssd/wangweihang/LLaMA-Factory/examples/train_full/qwen25_full_pretrain.yaml