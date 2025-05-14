from vllm import LLM, SamplingParams
import json
import os
from transformers import AutoTokenizer
import argparse

def run_model(model_path, cuda_device):
    # Set CUDA device
    # os.environ["CUDA_VISIBLE_DEVICES"] = str(cuda_device)
    
    # Sample prompts
    with open("data/test/ai_test_rebuild.json") as f:
        data = json.load(f)
    
    # Use model path directly
    model = model_path
    model_name = model.split('/')[-1]
    print(f"Running model {model_name} on CUDA:{cuda_device}")
    
    # Create sampling params
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=8192)
    
    # Initialize LLM with the specified model
    llm = LLM(model=model, tensor_parallel_size=8)
    tokenizer = AutoTokenizer.from_pretrained(model)

    # Prepare prompts
    template = """
你是一位专业的prompt工程师，擅长将混乱的项目需求转化为结构清晰的prompt。

请将下方``输入区``的混乱工程项目prompt重新格式化，使其更易于大模型理解和执行。直接输出格式化后的结果，不要有其他的描述。

``输入区``
{text}
``输入区结束``

请按照以下确切格式重新组织上述内容：

- 使用明确的标题【项目基本信息】，并在下方以列表形式呈现：
   - 项目名称：xxx
   - 项目年份：xxx
   - 项目分类：xxx
   - 项目性质：xxx
   - 项目所在地：xxx

- 建设规模、招标范围相关的内容，直接删除

- 使用标题【包含要点】，将需要包含的要点列点说明，如果未提供，则为“- 未提供”

- 使用标题【任务要求】，明确说明：
   - 删除原文中的具体章节编号（如"3.6.6"），只保留主题名称（如"电梯工程质量控制措施"）
   - 字数要求（如"900字左右"）

- 删除任何重复信息。

- 整体使用简洁明了的语言，避免冗长描述。

下面是一个完整的格式化实例，包含原文和格式化后的内容：

``原始prompt示例``
有一个工程名称为"滨海新区沧海未来社区B区块施工"的项目，2024年的，项目分类：房建/住宅，项目性质：新建,项目所在地：浙江省绍兴市，建设规模："滨海新区沧海未来社区B区块施工图纸范围内的地下室、基坑围护、桩基、地上建筑、室外工程，包括场地平整、土建(含桩基、基坑围护、地上及地下建筑结构)、安装（电气、消防电、给排水、消防水、暖通、防排烟、智能化、电梯）、公共区域精装修、幕墙专业工程、市政景观工程及室外水电工程；不包括变配电专业工程、燃气接入工程等，具体范围详见图纸及标底"，招标范围："滨海新区沧海未来社区B区块施工图纸范围内的地下室、基坑围护、桩基、地上建筑、室外工程，包括场地平整、土建(含桩基、基坑围护、地上及地下建筑结构)、安装（电气、消防电、给排水、消防水、暖通、防排烟、智能化、电梯）、公共区域精装修、幕墙专业工程、市政景观工程及室外水电工程；不包括变配电专业工程、燃气接入工程等，具体范围详见图纸及标底。"，方案分类：施工方案/机电安装/电梯。目前需要写3.6.6电梯工程质量控制措施，字数900字左右，请你进行写作。包含要点：安全管理方针\n安全管理目标\n管理机构\n危险源辨识与控制\n安全管理制度\nESHS管措施

``格式化后的prompt示例``
【项目基本信息】
- 项目名称：滨海新区沧海未来社区B区块施工
- 项目年份：2024年
- 项目分类：房建/住宅
- 项目性质：新建
- 项目所在地：浙江省绍兴市

【方案分类】
- 施工方案/机电安装/电梯

【包含要点】
- 安全管理方针
- 安全管理目标
- 管理机构
- 危险源辨识与控制
- 安全管理制度
- ESHS管措施

【任务要求】
- 编写"电梯工程质量控制措施"部分
- 字数要求900字左右。

``你的输出（从“【项目基本信息】”开始）``
"""
    prompts = []
    for item in data:
        prompt = item['question']
        messages = [
            # {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
            # {"role": "user", "content": template.format(text=prompt)}
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
    with open(f"data/test/test_output/0426/{model_name}.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Results saved to {model_name}.json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run inference on a specific model with a specific CUDA device')
    parser.add_argument('--model_path', type=str, required=True, help='Full path to the model')
    parser.add_argument('--cuda_device', type=int, required=True, help='CUDA device number (0-8)')
    
    args = parser.parse_args()
    
    # Run the model on the specified CUDA device
    run_model(args.model_path, args.cuda_device)