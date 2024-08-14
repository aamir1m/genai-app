import transformers
import torch
from transformers import AutoTokenizer

# Use CPU only
device = torch.device("cpu")

model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation",
    model = model,
    torch_dtype = torch.float16,
    device=device.index,
)

sequences = pipeline(
    "what shall i cook for dinner \n",
    do_sample = True,
    top_k = 10,
    num_return_sequences = 1,
    eos_token_id = tokenizer.eos_token_id,
    truncation = True,
    max_length = 400
)

for seq in sequences:
    print(f"result: {seq['generate_text']}")