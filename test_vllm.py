from vllm import LLM, SamplingParams

prompts = [
    "你是谁？"
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

path = "/home/lt_08321/hdd/wangweihang/outputs/saves/qwen2.5-14b/full/pretrain_sft_241202"
llm = LLM(model=path)

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")