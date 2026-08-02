# HF Model Recommendations for ASP Extraction

## Requirements

The extraction model must:
- Classify web pages into types (homepage, listing, detail, search, checkout, account, documentation)
- Extract form semantics and candidate actions from HTML
- Run locally on consumer GPU (8-24GB VRAM) or CPU
- Be quantized to 4-bit or 8-bit for inference speed
- Handle HTML/text input up to 4-8k tokens
- Be licensed for commercial use (Apache-2.0, MIT, BSD)

## Recommended Models

### Primary: SmolLM2-1.7B-Instruct (HuggingFaceTB/SmolLM2-1.7B-Instruct)
- **Size**: 1.7B parameters → ~1GB at 4-bit (GGUF)
- **Context**: 8192 tokens
- **License**: Apache-2.0
- **Strengths**: Strong instruction following, trained on code and structured data, excellent for JSON output
- **Quantization**: Available as GGUF on HF Hub (Q4_K_M, Q8_0)
- **Inference**: llama.cpp, ollama, vLLM, transformers
- **Why**: Smallest viable model for structured extraction with reliable JSON output

### Alternative: Qwen2.5-1.5B-Instruct (Qwen/Qwen2.5-1.5B-Instruct)
- **Size**: 1.5B parameters → ~0.9GB at 4-bit
- **Context**: 32768 tokens (can fit full page + prompt)
- **License**: Apache-2.0
- **Strengths**: Excellent multilingual, strong structured output, large context
- **Quantization**: GGUF widely available
- **Why**: Larger context helps with full-page HTML input

### Alternative: Phi-3.5-mini-instruct (microsoft/Phi-3.5-mini-instruct)
- **Size**: 3.8B parameters → ~2.3GB at 4-bit
- **Context**: 128k tokens
- **License**: MIT
- **Strengths**: Strong reasoning, excellent instruction following, large context
- **Quantization**: GGUF available
- **Why**: Higher quality if VRAM budget allows 3GB+

### For CPU-only / Very Constrained: SmolLM2-360M-Instruct (HuggingFaceTB/SmolLM2-360M-Instruct)
- **Size**: 360M → ~200MB at 4-bit
- **Context**: 8192 tokens
- **License**: Apache-2.0
- **Strengths**: Tiny, fast, runs on CPU in seconds
- **Tradeoff**: Lower accuracy on complex extraction
- **Why**: Fallback for CPU-only CI or edge deployment

## Prompting Strategy

Use a structured prompt that asks for JSON output matching a simplified schema:

```json
{
  "page_type": "homepage|listing|detail|search|checkout|account|documentation|other",
  "confidence": 0.0-1.0,
  "forms": [
    {"action": "/submit", "method": "POST", "fields": [{"name": "email", "type": "email", "required": true}]}
  ],
  "candidate_actions": [
    {"name": "search_products", "description": "Search for products", "selector_hint": "form[action*='search']"}
  ],
  "navigation": {"primary_links": ["/products", "/about", "/contact"]}
}
```

Fine-tuning on a small dataset of labeled pages (100-500) would significantly improve accuracy.

## Download Commands

```bash
# SmolLM2-1.7B (recommended primary)
huggingface-cli download HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF --local-dir ./models/smollm2-1.7b

# Qwen2.5-1.5B (alternative)
huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct-GGUF --local-dir ./models/qwen2.5-1.5b

# Phi-3.5-mini (higher quality)
huggingface-cli download microsoft/Phi-3.5-mini-instruct-GGUF --local-dir ./models/phi-3.5-mini
```

## Evaluation Plan

1. Create test set: 50 pages spanning all 7 types, manually labeled
2. Run each model with identical prompt
3. Measure: page_type accuracy, form field F1, action extraction precision/recall
4. Select best model for Phase II integration

## Integration Notes

- Model runs as a subprocess or via llama.cpp Python bindings
- Batch pages in groups of 8-16 for throughput
- Cache embeddings for repeated pages
- Fallback to heuristics if model confidence < 0.5