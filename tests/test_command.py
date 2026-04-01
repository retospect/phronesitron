"""Tests for phronesitron CLI."""

from phronesitron.cli import _parse_model, _resolve_mcp, _wrap_text, build_parser


def test_parser_help_shows_mcp():
    """Parser includes --mcp flag."""
    parser = build_parser()
    help_text = parser.format_help()
    assert "--mcp" in help_text
    assert "--model" in help_text


def test_parse_model_default():
    assert _parse_model(None) == ("ollama", "qwen3.5:9b")


def test_parse_model_bare_name():
    assert _parse_model("llama3") == ("ollama", "llama3")


def test_parse_model_with_provider():
    assert _parse_model("anthropic/claude-sonnet-4-20250514") == (
        "anthropic",
        "claude-sonnet-4-20250514",
    )


def test_parse_model_openai():
    assert _parse_model("openai/gpt-4o") == ("openai", "gpt-4o")


def test_resolve_mcp_shortcut():
    server = _resolve_mcp("precis")
    assert server.name == "precis"
    assert "precis-mcp" in server.cmd[-1]


def test_resolve_mcp_raw_command():
    server = _resolve_mcp("python -m my_server")
    assert server.cmd == ["python", "-m", "my_server"]
    assert server.name == "my_server"


def test_wrap_text_preserves_paragraphs():
    text = "short\n\nAlso short"
    result = _wrap_text(text)
    assert "\n\n" in result


def test_wrap_text_wraps_long_lines():
    text = "word " * 30
    result = _wrap_text(text.strip())
    lines = result.split("\n")
    assert all(len(line) <= 80 for line in lines)


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["hello", "world"])
    assert args.question == ["hello", "world"]
    assert args.model is None
    assert args.mcp == []
    assert args.temperature == 0.7
    assert args.max_tokens == 4096
    assert args.no_think is False
    assert args.unformatted is False


def test_parser_mcp_repeatable():
    parser = build_parser()
    args = parser.parse_args(["--mcp", "precis", "--mcp", "perplexity", "query"])
    assert args.mcp == ["precis", "perplexity"]
