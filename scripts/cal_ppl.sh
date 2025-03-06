#!/bin/bash

torchrun --nproc_per_node=1 \
    scripts/cal_ppl.py \
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    --model_name_or_path bidding_outputs/finetune_outputs/qwen_pretrain_finetune_241230 \
    --dataset bidding_test_ppl \
=======
    --model_name_or_path /home/lt_08321/hdd/wangweihang/outputs/saves/241216/qwen2.5-14b/full/pt \
    --dataset pretrain_241216 \
>>>>>>> ad1c2617 (bidding)
=======
    --model_name_or_path /home/lt_08321/hdd/wangweihang/outputs/saves/241216/qwen2.5-14b/full/pt \
    --dataset pretrain_241216 \
>>>>>>> 6b4f8743 (merge)
=======
    --model_name_or_path bidding_outputs/finetune_outputs/qwen_pretrain_finetune_241230 \
    --dataset bidding_test_ppl \
>>>>>>> 7b37eebd (bidding pretrain+finetune)
    --batch_size 1 \
    --template qwen \
    --cutoff_len 4096 \
    --stage pt \
    --save_name ppl.json