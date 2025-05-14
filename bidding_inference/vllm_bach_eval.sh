#!/bin/bash

# 定义模型路径列表
declare -a MODEL_PATHS=(
    "bidding_outputs/finetune_outputs/sft@14B@pt@full@Wrting@250415"
    # "bidding_outputs/finetune_outputs/sft@72B@lora_merge@QA@250407"
    # "bidding_outputs/finetune_outputs/sft@14B@pt@full@GIRCS@250306"
    # "bidding_outputs/finetune_outputs/sft@14B@pt@full@GIRCS@250312"
    # "bidding_outputs/posttrain_outputs/dpo@14B@pt@full@GIRCS@250312"
    # "bidding_outputs/finetune_outputs/sft@14B@pure@full@GIRCS@250227"
)

# 检查可用的CUDA设备数量（这里假设您有9个设备，从0到8）
MAX_CUDA_DEVICES=8

# 计算要运行的模型数量
NUM_MODELS=${#MODEL_PATHS[@]}
echo "共有 $NUM_MODELS 个模型需要运行"

# 检查是否有足够的CUDA设备
if [ $NUM_MODELS -gt $MAX_CUDA_DEVICES ]; then
    echo "警告：模型数量 ($NUM_MODELS) 超过了可用的CUDA设备数量 ($MAX_CUDA_DEVICES)"
    echo "部分模型将无法并行运行"
fi

# 启动每个模型的推理进程
for ((i=0; i<$NUM_MODELS; i++)); do
    # 获取模型路径
    MODEL_PATH="${MODEL_PATHS[$i]}"
    
    # 分配CUDA设备（确保不超过最大设备数量）
    CUDA_DEVICE=$((i % MAX_CUDA_DEVICES))
    
    echo "启动模型 $(basename "$MODEL_PATH") 在 CUDA:$CUDA_DEVICE 上..."
    
    # 启动Python脚本作为后台进程
    python process/vllm_batch_infer.py --model_path "$MODEL_PATH" --cuda_device $CUDA_DEVICE &
    
    # 存储进程ID
    PIDS+=($!)
    
    echo "进程已启动，PID: ${PIDS[-1]}"
done

echo "所有模型推理进程已启动"

# 等待所有后台进程完成
echo "等待所有进程完成..."
wait

echo "所有模型推理已完成"