"""One-shot LLM CLI with optional MCP tool support.

Usage:
    ph "explain quantum tunneling"
    ph -m anthropic/claude-sonnet-4-20250514 "summarize this" < paper.txt
    ph --mcp precis "what papers do we have on chlorine evolution?"
    echo "some text" | ph "rewrite this formally"
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import textwrap as tr

from acatome_lambic.core.config import LlmConfig, McpServer, ShellConfig
from acatome_lambic.core.session import ChatSession
from termcolor import colored

# Well-known MCP servers — shortcuts for --mcp flag
_MCP_SHORTCUTS: dict[str, list[str]] = {
    "precis": ["uvx", "precis-mcp"],
    "perplexity": ["uvx", "perplexity-sonar-mcp"],
    "gripe": ["uvx", "gripe-mcp"],
}


def _resolve_mcp(name: str) -> McpServer:
    """Resolve an MCP server name to a McpServer config.

    Accepts either a shortcut name (e.g. 'precis') or a command
    (e.g. 'uvx precis-mcp' or 'python -m my_server').
    """
    if name in _MCP_SHORTCUTS:
        return McpServer(name=name, cmd=_MCP_SHORTCUTS[name])
    # Treat as a raw command
    parts = name.split()
    short = parts[-1].split("/")[-1]  # last component for display
    return McpServer(name=short, cmd=parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ph",
        description="One-shot LLM query with optional MCP tools.",
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Question or prompt (also reads stdin if piped)",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=None,
        help="LLM model spec: 'provider/model' or just 'model' for ollama "
        "(default: ollama/qwen3.5:9b)",
    )
    parser.add_argument(
        "--mcp",
        action="append",
        default=[],
        metavar="SERVER",
        help="Enable MCP server (shortcut or command). Repeatable. "
        f"Shortcuts: {', '.join(sorted(_MCP_SHORTCUTS))}",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Max output tokens (default: 4096)",
    )
    parser.add_argument(
        "--no-think",
        action="store_true",
        help="Disable reasoning/thinking mode",
    )
    parser.add_argument(
        "-u",
        "--unformatted",
        action="store_true",
        help="Don't word-wrap output",
    )
    parser.add_argument(
        "-s",
        "--system",
        type=str,
        default="",
        help="System prompt",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show tool calls and metadata",
    )
    return parser


def _parse_model(spec: str | None) -> tuple[str, str]:
    """Parse 'provider/model' → (provider, model). Bare name → ollama."""
    if spec is None:
        return "ollama", "qwen3.5:9b"
    if "/" in spec:
        provider, model = spec.split("/", 1)
        return provider, model
    return "ollama", spec


def _wrap_text(text: str) -> str:
    """Word-wrap paragraphs for terminal output."""
    paragraphs = text.split("\n")
    wrapped = []
    for para in paragraphs:
        if para.strip():
            wrapped.append("\n".join(tr.wrap(para, width=80, replace_whitespace=False)))
        else:
            wrapped.append("")
    return "\n".join(wrapped)


async def _run(args: argparse.Namespace) -> int:
    """Async entry point."""
    # Collect prompt from args + stdin
    parts = []
    if args.question:
        parts.append(" ".join(args.question))
    if not sys.stdin.isatty():
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            parts.append(stdin_text)

    if not parts:
        print("No prompt provided. Use: ph 'your question here'", file=sys.stderr)
        return 1

    prompt = "\n\n".join(parts)

    # Build config
    provider, model = _parse_model(args.model)
    llm_config = LlmConfig(
        provider=provider,
        model=model,
        think=not args.no_think,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    servers = [_resolve_mcp(name) for name in args.mcp]

    config = ShellConfig(
        llm=llm_config,
        servers=servers,
        system_prompt=args.system,
    )

    session = ChatSession(config)
    use_color = not args.no_color and sys.stdout.isatty()

    try:
        status = await session.start()

        if not status["llm_ok"]:
            print(
                f"Error: cannot reach LLM ({llm_config.spec}). "
                "Is the provider running?",
                file=sys.stderr,
            )
            return 1

        if args.verbose:
            srv_info = status.get("servers", {})
            for name, st in srv_info.items():
                icon = "●" if st == "connected" else "○"
                print(
                    colored(f"  {icon} {name}: {st}", "blue")
                    if use_color
                    else f"  {icon} {name}: {st}",
                    file=sys.stderr,
                )
            n_tools = status.get("tools", 0)
            if n_tools:
                print(
                    colored(f"  {n_tools} tools available", "blue")
                    if use_color
                    else f"  {n_tools} tools available",
                    file=sys.stderr,
                )

        # Run the one-shot turn
        collected = ""
        async for event in session.turn(prompt):
            if event.kind == "text":
                collected += event.data

            elif event.kind == "tool_result" and args.verbose:
                tr_data = event.data
                name = tr_data.call.name
                elapsed = tr_data.elapsed
                trunc = " (truncated)" if tr_data.truncated else ""
                line = f"  ← {name} ({elapsed:.1f}s){trunc}"
                print(colored(line, "blue") if use_color else line, file=sys.stderr)

            elif event.kind == "thinking" and args.verbose:
                lines = event.data.strip().split("\n")
                preview = lines[0][:80] + ("…" if len(lines[0]) > 80 else "")
                print(
                    colored(f"  💭 {preview}", "cyan")
                    if use_color
                    else f"  (thinking) {preview}",
                    file=sys.stderr,
                )

            elif event.kind == "error":
                print(f"Error: {event.data}", file=sys.stderr)
                return 1

            elif event.kind == "usage" and args.verbose:
                u = event.data
                line = (
                    f"  tokens: {u['prompt_tokens']}→{u['completion_tokens']} "
                    f"stop: {u['stop_reason']}"
                )
                print(colored(line, "blue") if use_color else line, file=sys.stderr)

        # Format and print output
        if collected.strip():
            output = collected.strip()
            if not args.unformatted:
                output = _wrap_text(output)
            if use_color:
                print(colored(output, "green"))
            else:
                print(output)

        return 0

    finally:
        await session.close()


def main() -> None:
    parser = build_parser()
    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    sys.exit(asyncio.run(_run(args)))


if __name__ == "__main__":
    main()
