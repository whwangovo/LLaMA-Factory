#!/bin/bash

torchrun --nproc_per_node=1 \
    scripts/cal_ppl.py \
    --model_name_or_path bidding_outputs/finetune_outputs/qwen_pretrain_finetune_241230 \
    --dataset bidding_test_ppl \
    --batch_size 1 \
    --template qwen \
    --cutoff_len 4096 \
    --stage pt \
    --save_name ppl.json