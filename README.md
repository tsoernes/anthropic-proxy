# Anthropic Proxy

A LiteLLM-based proxy that transforms Anthropic API requests to Azure OpenAI deployments.

## Features

- **Anthropic API compatibility**: Exposes `/v1/messages` endpoint compatible with Anthropic SDK
- **Azure backend**: Routes requests to Azure OpenAI deployments
- **Rich dashboard**: Real-time stats with session/today/week/month/all-time breakdowns
- **Persistent statistics**: Usage stats saved to JSON and survive restarts
- **Cost tracking**: Per-model pricing with regex pattern matching
- **Request logging**: Optional debug logging with sanitization
- **Graceful shutdown**: SIGINT/SIGTERM handling with stats save
- **Headless mode**: Run without dashboard for production

## Installation

```bash
# Clone and run with uv
uv run --script antropic_proxy
```

## Configuration

Create a `.env` file:

```env
AZURE_API_KEY=your-azure-api-key
AZURE_API_BASE=https://your-resource.openai.azure.com
AZURE_API_VERSION=2024-07-01-preview
```

### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `PROXY_DEBUG_LOG` | Path to debug log file (rotates at 10MB) |
| `PROXY_HEADLESS` | Set to `1` or `true` to disable dashboard |
| `PERSISTENT_STATS_FILE` | Path to stats JSON (default: `persistent_stats.json`) |
| `PERSISTENT_DAILY_RETENTION_DAYS` | Days to keep daily stats (default: 90) |
| `PERSISTENT_WEEKLY_RETENTION_WEEKS` | Weeks to keep weekly stats (default: 52) |
| `PERSISTENT_MONTHLY_RETENTION_MONTHS` | Months to keep monthly stats (default: 36) |

## Usage

```bash
# Run with default model (Kimi-K2.5)
uv run --script antropic_proxy

# Run with specific model
uv run --script antropic_proxy GPT-5.1-codex-mini

# Run on different port
uv run --script antropic_proxy --port 8080

# Headless mode (no dashboard)
PROXY_HEADLESS=1 uv run --script antropic_proxy

# With debug logging
PROXY_DEBUG_LOG=proxy.log uv run --script antropic_proxy
```

## API Usage

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="sk-anything",
    base_url="http://localhost:4142",
)

response = client.messages.create(
    model="claude-sonnet-4.6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Pricing Configuration

Built-in pricing patterns (per 1M tokens):

| Model Pattern | Input | Output | Cached Input |
|--------------|-------|--------|--------------|
| Kimi-K2.5 | $0.60 | $3.00 | $0.00 |
| GPT-5.x-codex | $1.25 | $10.00 | $0.13 |
| GPT-5.x-codex-mini | $0.25 | $2.00 | $0.03 |
| GPT-5.x | $1.25 | $10.00 | $0.13 |

Patterns use regex matching for version numbers (e.g., `gpt-5.1`, `gpt-5.2`).

## Dashboard Stats

The dashboard shows:
- **Requests**: Total API calls
- **Tokens**: Prompt, completion, and reasoning tokens
- **Avg RPM/TPM**: Average rates since period start
- **RPM/TPM (last minute)**: Rolling 60-second window
- **Avg latency**: Response time averages
- **Estimated cost**: Total cost per period

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run linters
basedpyright antropic_proxy
ruff check antropic_proxy
```

## License

MIT
