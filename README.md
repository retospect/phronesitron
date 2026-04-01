[![check](https://github.com/retospect/phronesitron/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/phronesitron/actions/workflows/check.yml)
[![PyPI version](https://badge.fury.io/py/phronesitron.svg)](https://badge.fury.io/py/phronesitron)

# Phronesitron

One-shot LLM CLI with optional MCP tool support.
Uses any LLM provider (Ollama, OpenAI, Anthropic, …) via [acatome-lambic](https://github.com/retospect/acatome-lambic).

## Quick start

```bash
# Simple query (default: ollama/qwen3.5:9b)
ph explain quantum tunneling in 3 sentences

# Use a different model
ph -m anthropic/claude-sonnet-4-20250514 "summarize this" < paper.txt

# Pipe input
echo "some text" | ph rewrite this formally

# With MCP tools — the LLM can search your paper library
ph --mcp precis "what papers do we have on chlorine evolution?"

# Multiple MCP servers
ph --mcp precis --mcp perplexity "compare our MOF results to recent literature"
```

## Install

```bash
pip install phronesitron
# or with litellm for non-Ollama providers:
pip install "phronesitron[litellm]"
```

For Ollama (default), make sure `ollama` is running locally.
For OpenAI/Anthropic, set the usual env vars (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).

## Options

```
ph [options] <question...>

  -m, --model MODEL      provider/model (default: ollama/qwen3.5:9b)
  --mcp SERVER           enable MCP server (repeatable)
  -t, --temperature T    sampling temperature (default: 0.7)
  --max-tokens N         max output tokens (default: 4096)
  --no-think             disable reasoning mode
  -u, --unformatted      don't word-wrap output
  -s, --system PROMPT    system prompt
  --no-color             disable colored output
  -v, --verbose          show tool calls and metadata
```

### MCP shortcuts

Built-in shortcut names for `--mcp`:

- **precis** — `uvx precis-mcp` (paper library)
- **perplexity** — `uvx perplexity-sonar-mcp` (web search)
- **gripe** — `uvx gripe-mcp` (issue tracking)

You can also pass a full command: `--mcp "python -m my_server"`.

