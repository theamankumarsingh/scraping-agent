# scraping-agent

A CLI tool that uses an Ollama model (local or remote) to search websites and scrape information.

## About

`scraping-agent` helps you automate web lookup and data extraction from the command line.

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

## License

Apache License 2.0. See [LICENSE](./LICENSE).

## Authors

[![Contributors](https://contrib.rocks/image?repo=theamankumarsingh/scraping-agent)](https://github.com/theamankumarsingh/scraping-agent/graphs/contributors)
