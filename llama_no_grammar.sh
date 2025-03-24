 # llama-server -m ~/Code/models/gemma-3-12b-it-Q8_0.gguf -c 12288 -n 128 -np 2 --temp 0.8
 llama-server -m ~/Code/models/gemma-3-12b-it-Q8_0.gguf -md ~/Code/models/gemma-3-1b-it-Q8_0.gguf -c 12288 --temp 1.0 --top-k 64 --top-p 0.95 --min-p 0.01 -n 128 -np 2 --samplers "top_k;top_p;min_p;temperature"
