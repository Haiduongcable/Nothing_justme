
# from transformers import AutoModelForCausalLM, AutoTokenizer
# cache_dir = "/hdd4/duongnh/project/ZaloMath2023/pretrained"
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-14B", device_map="auto", trust_remote_code=True, cache_dir="qween").eval()
from transformers import AutoModelForCausalLM, AutoTokenizer
cache_dir = "/hdd4/duongnh/project/ZaloMath2023/pretrained"
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B", device_map="auto", trust_remote_code=True, cache_dir=cache_dir).eval()