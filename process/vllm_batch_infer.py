from vllm import LLM, SamplingParams
import json
import os
import torch
from transformers import AutoTokenizer
import argparse

def run_model(model_path, cuda_device):
    # Set CUDA device
    os.environ["CUDA_VISIBLE_DEVICES"] = str(cuda_device)
    
    # Sample prompts
    with open("data/test/ai_test_set.json") as f:
        data = json.load(f)
    
    # Use model path directly
    model = model_path
    model_name = model.split('/')[-1]
    print(f"Running model {model_name} on CUDA:{cuda_device}")
    
    # Create sampling params
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=8192)
    
    # Initialize LLM with the specified model
    llm = LLM(model=model)
    tokenizer = AutoTokenizer.from_pretrained(model)

    # Prepare prompts
    prompts = []
    for item in data:
        prompt = item['question']
        messages = [
            {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        prompts.append(text)

    # Generate texts from the prompts
    outputs = llm.generate(prompts, sampling_params)
    
    # Process results
    results = []
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
        results.append({
            'input': prompt,
            'output': generated_text
        })

    # Save results to a JSON file
    with open(f"data/test/test_output/0313/{model_name}.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)
    
    print(f"Results saved to {model_name}.json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run inference on a specific model with a specific CUDA device')
    parser.add_argument('--model_path', type=str, required=True, help='Full path to the model')
    parser.add_argument('--cuda_device', type=int, required=True, help='CUDA device number (0-8)')
    
    args = parser.parse_args()
    
    # Run the model on the specified CUDA device
    run_model(args.model_path, args.cuda_device)