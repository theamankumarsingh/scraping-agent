# scraping-agent

A CLI web **researcher and scraper** powered by Ollama models (local or remote).

## About

`scraping-agent` automates iterative web research and scraping from the command line:

- breaks the objective into smaller unresolved tasks,
- searches and browses relevant pages,
- extracts evidence-backed findings with source URLs,
- tracks remaining unresolved tasks against the overall objective,
- and stops when research is complete (or iteration limits are reached).

## Current implementation

### System architecture (simplified)

```text
CLI Prompt
   │
   ▼
main.py
   │
   ▼
research() orchestrator
   │
   ▼
ResearchState initialized (objective, unresolved=[objective])
   │
   ▼
Planner (LLM only) -> try break objective into smaller unresolved tasks
   │
   ▼
Research Agent (LLM + Browser) -> ResearchResult
   │
   ▼
Task Checker (LLM only) -> IntrospectionResult
   │
   ▼
unresolved empty OR max_iterations reached?
   ├─ Yes -> Final ResearchState JSON
   └─ No  -> Research again
```

## Dependencies

- Python `3.12`
- [uv](https://docs.astral.sh/uv/) (package manager)
- [Ollama](https://ollama.com/) server running locally or remotely
- Python package: `browser-use`

## Install

```bash
git clone https://github.com/theamankumarsingh/scraping-agent.git
cd scraping-agent
uv sync
```

## Usage

1. Start Ollama (if not already running):

```bash
ollama serve
```

2. Pull a model (example):

```bash
ollama pull qwen3.5:4b
```

3. (Optional) If using a remote Ollama server, set its URL:

```bash
export OLLAMA_BASE_URL="http://your-ollama-host:11434"
```

4. Run the agent:

```bash
uv run scraping-agent --model "qwen3.5:4b" --prompt "Who is the current president of India?"
```

The CLI prints the final `ResearchState` as formatted JSON.

## License

Apache License 2.0. See [LICENSE](./LICENSE).

## Authors

[![Contributors](https://contrib.rocks/image?repo=theamankumarsingh/scraping-agent)](https://github.com/theamankumarsingh/scraping-agent/graphs/contributors)
