"""Generate self-hosted SVG profile telemetry and flagship project cards from GitHub GraphQL."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

GRAPHQL_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    name
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoryContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
    repositories(
      first: 100
      ownerAffiliations: [OWNER]
      isFork: false
      privacy: PUBLIC
    ) {
      totalCount
      nodes {
        name
        description
        stargazerCount
        forkCount
        primaryLanguage {
          name
          color
        }
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
  domainAi: repository(owner: "seniruvitharanage", name: "domain-ai") {
    name
    nameWithOwner
    description
    stargazerCount
    forkCount
    primaryLanguage {
      name
      color
    }
  }
}
"""

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

FEATURED_SPECS = [
    {
        "slug": "localgravity",
        "owner": "Thush099",
        "repo": "LocalGravity",
        "title": "LocalGravity · macOS AI",
        "line1": "Swift WKWebView & zero-dep Node.js hub for Ollama & cloud",
        "line2": "models · 47 Mac & web tools, SVG telemetry & Artifact Canvas.",
        "metric": "0 Deps · 284 Tests",
        "metric_color": "#38BDF8",
        "tag": "macOS · Local LLMs",
    },
    {
        "slug": "veridoc",
        "owner": "Thush099",
        "repo": "veridoc-forensics",
        "title": "veridoc-forensics · OCR & NLI",
        "line1": "OpenCV skew/blur restoration, JPEG ELA tamper detection,",
        "line2": "Tesseract OCR & hybrid BM25/TF-IDF claim verification UI.",
        "metric": "100.0% Restored OCR",
        "metric_color": "#34D399",
        "tag": "CV · Document Forensics",
    },
    {
        "slug": "traceguard",
        "owner": "Thush099",
        "repo": "traceguard-eval",
        "title": "traceguard-eval · Agent Eval",
        "line1": "Deterministic tool-using agent benchmark, adversarial",
        "line2": "injection/fault fuzzer, FastAPI replay UI & 42 pytest checks.",
        "metric": "100.00 Audit Score",
        "metric_color": "#818CF8",
        "tag": "Agents · Safety Fuzzing",
    },
    {
        "slug": "cm3604",
        "owner": "Thush099",
        "repo": "CM3604_CW",
        "title": "CM3604_CW · FActScore NLI",
        "line1": "Automated LLM claim fact-checking comparing BM25 lexical",
        "line2": "overlap against fine-tuned DeBERTa textual entailment.",
        "metric": "88.24% Accuracy",
        "metric_color": "#FBBF24",
        "tag": "NLP · Fact Verification",
    },
    {
        "slug": "decodelabs",
        "owner": "Thush099",
        "repo": "DecodeLabs-Internship",
        "title": "DecodeLabs-Internship",
        "line1": "Applied AI engineering capstones: query guardrails, customer",
        "line2": "classification, TF-IDF tech recommender, OpenCV OCR.",
        "metric": "4 End-to-End Pipelines",
        "metric_color": "#38BDF8",
        "tag": "Internship · Applied AI",
    },
    {
        "slug": "domain-ai",
        "owner": "seniruvitharanage",
        "repo": "domain-ai",
        "title": "domain-ai · Task Priority ML",
        "line1": "Developer task urgency classifier trained on 9,120 samples",
        "line2": "with TF-IDF text & metadata features in Gradient Boosting.",
        "metric": "96.97% Test F1",
        "metric_color": "#34D399",
        "tag": "Collaborative · ML",
    },
]


def fetch_github_stats(username: str, token: str) -> dict[str, Any]:
    """Fetch public profile contribution and repository metrics via GitHub GraphQL."""
    payload = json.dumps({"query": QUERY, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{username}-profile-generator",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if "errors" in data:
        raise RuntimeError(f"GitHub GraphQL errors: {data['errors']}")
    return data


def _heat_color(count: int) -> str:
    if count <= 0:
        return "#161B22"
    if count <= 2:
        return "#0E4429"
    if count <= 5:
        return "#006D32"
    if count <= 10:
        return "#26A641"
    return "#39D353"


def compute_streaks(calendar: dict[str, Any]) -> tuple[int, int]:
    """Compute (current_streak_days, longest_streak_days) from the contribution calendar."""
    days: list[tuple[str, int]] = []
    for week in calendar.get("weeks", []):
        for day in week.get("contributionDays", []):
            days.append((str(day["date"]), int(day["contributionCount"])))

    longest = 0
    running = 0
    for _, count in days:
        if count > 0:
            running += 1
            if running > longest:
                longest = running
        else:
            running = 0

    current = 0
    if days:
        idx = len(days) - 1
        # Allow today (last slot) to still be 0 before the first commit of the day
        if days[idx][1] == 0:
            idx -= 1
        while idx >= 0 and days[idx][1] > 0:
            current += 1
            idx -= 1

    return current, longest


def build_stats_svg(data: dict[str, Any]) -> str:
    """Render a 900x268 self-hosted dark-slate GitHub Activity + Language SVG card."""
    user = data["data"].get("user") or data["data"]["viewer"]
    contrib = user["contributionsCollection"]
    calendar = contrib["contributionCalendar"]
    total_contributions = int(calendar["totalContributions"])
    total_commits = int(contrib["totalCommitContributions"])
    total_prs = int(contrib["totalPullRequestContributions"])
    current_streak, longest_streak = compute_streaks(calendar)

    repos = [r for r in user["repositories"]["nodes"] if not r.get("isPrivate", False)]
    public_repo_count = int(user["repositories"].get("totalCount") or len(repos))
    total_stars = sum(int(r["stargazerCount"]) for r in repos)

    lang_repo_counts: dict[str, dict[str, Any]] = {}
    for r in repos:
        pl = r.get("primaryLanguage")
        if pl and pl.get("name"):
            name = pl["name"]
            color = pl.get("color") or "#38BDF8"
            entry = lang_repo_counts.setdefault(name, {"repos": 0, "color": color})
            entry["repos"] += 1
        elif r.get("languages", {}).get("edges"):
            top_edge = r["languages"]["edges"][0]["node"]
            name = top_edge["name"]
            color = top_edge.get("color") or "#38BDF8"
            entry = lang_repo_counts.setdefault(name, {"repos": 0, "color": color})
            entry["repos"] += 1

    code_bytes: dict[str, dict[str, Any]] = {}
    for r in repos:
        for edge in r.get("languages", {}).get("edges", []):
            name = edge["node"]["name"]
            color = edge["node"].get("color") or "#818CF8"
            size = int(edge["size"])
            # Cap oversized raw ipynb JSON so source code repositories remain proportionally visible
            effective_size = min(size, 45000) if name == "Jupyter Notebook" else size
            entry = code_bytes.setdefault(name, {"bytes": 0, "color": color, "repos": 0})
            entry["bytes"] += effective_size

    for name, info in lang_repo_counts.items():
        if name in code_bytes:
            code_bytes[name]["repos"] = info["repos"]

    sorted_langs = sorted(
        code_bytes.items(),
        key=lambda kv: kv[1]["bytes"],
        reverse=True,
    )[:5]
    total_lang_bytes = max(sum(v["bytes"] for _, v in sorted_langs), 1)

    # 28-week contribution strip (28 cols x 7 rows -> 389px wide)
    weeks = calendar["weeks"][-28:]
    heatmap_cells = []
    start_x, start_y = 28, 150
    cell_size, gap = 11, 3
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week["contributionDays"]):
            cx = start_x + w_idx * (cell_size + gap)
            cy = start_y + d_idx * (cell_size + gap)
            fill = _heat_color(int(day["contributionCount"]))
            heatmap_cells.append(
                f'<rect x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill}" />'
            )

    legend_swatches = []
    for i, shade in enumerate(["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]):
        sx = 340 + i * 12
        legend_swatches.append(f'<rect x="{sx}" y="131" width="9" height="9" rx="2" fill="{shade}" />')

    # Stacked language bar (x=472, width=400)
    bar_x, bar_y, bar_w, bar_h = 472, 86, 400, 10
    bar_segments = []
    cur_x = float(bar_x)
    for idx, (name, info) in enumerate(sorted_langs):
        seg_w = (info["bytes"] / total_lang_bytes) * bar_w
        if idx == len(sorted_langs) - 1:
            seg_w = (bar_x + bar_w) - cur_x
        bar_segments.append(
            f'<rect x="{cur_x:.1f}" y="{bar_y}" width="{max(seg_w, 2.0):.1f}" height="{bar_h}" fill="{escape(info["color"])}" />'
        )
        cur_x += seg_w

    legend_rows = []
    for idx, (name, info) in enumerate(sorted_langs[:4]):
        pct = (info["bytes"] / total_lang_bytes) * 100.0
        col = idx % 2
        row = idx // 2
        lx = 472 + col * 204
        ly = 124 + row * 26
        repo_n = info.get("repos", 0)
        display_name = "Jupyter" if name == "Jupyter Notebook" else name
        suffix = f" ({repo_n}r)" if repo_n else ""
        right_x = lx + 196 if col == 1 else lx + 188
        legend_rows.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4.5" fill="{escape(info["color"])}" />'
            f'<text x="{lx + 16}" y="{ly}" fill="#E2E8F0" font-family="{FONT_SANS}" font-size="12" font-weight="500">{escape(display_name)}{escape(suffix)}</text>'
            f'<text x="{right_x}" y="{ly}" text-anchor="end" fill="#94A3B8" font-family="{FONT_SANS}" font-size="12">{pct:.1f}%</text>'
        )

    updated_label = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    return f"""<svg width="900" height="268" viewBox="0 0 900 268" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cardBg" x1="0" y1="0" x2="900" y2="268" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0D1117"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <clipPath id="langBarClip">
      <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5"/>
    </clipPath>
  </defs>

  <rect width="900" height="268" rx="14" fill="url(#cardBg)"/>
  <rect x="0.75" y="0.75" width="898.5" height="266.5" rx="13.25" stroke="#30363D" stroke-width="1.5"/>
  <line x1="446" y1="24" x2="446" y2="244" stroke="#1E293B" stroke-width="1.2"/>

  <!-- Left Panel: Live Telemetry -->
  <text x="28" y="38" fill="#F8FAFC" font-family="{FONT_SANS}" font-size="15" font-weight="700">
    GitHub Activity &amp; Streaks
  </text>
  <text x="422" y="38" text-anchor="end" fill="#64748B" font-family="{FONT_SANS}" font-size="11">
    Rolling 12 months
  </text>

  <!-- 4 Stat Tiles -->
  <rect x="28" y="54" width="93" height="62" rx="8" fill="#161B22" stroke="#1E293B"/>
  <text x="40" y="80" fill="#38BDF8" font-family="{FONT_SANS}" font-size="20" font-weight="700">{total_contributions}</text>
  <text x="40" y="101" fill="#94A3B8" font-family="{FONT_SANS}" font-size="11">Contributions</text>

  <rect x="129" y="54" width="93" height="62" rx="8" fill="#161B22" stroke="#1E293B"/>
  <text x="141" y="80" fill="#34D399" font-family="{FONT_SANS}" font-size="20" font-weight="700">{total_commits}</text>
  <text x="141" y="101" fill="#94A3B8" font-family="{FONT_SANS}" font-size="11">Commits</text>

  <rect x="230" y="54" width="93" height="62" rx="8" fill="#161B22" stroke="#1E293B"/>
  <text x="242" y="80" fill="#FBBF24" font-family="{FONT_SANS}" font-size="18" font-weight="700">{longest_streak}d / {current_streak}d</text>
  <text x="242" y="101" fill="#94A3B8" font-family="{FONT_SANS}" font-size="11">Max / Cur Streak</text>

  <rect x="331" y="54" width="91" height="62" rx="8" fill="#161B22" stroke="#1E293B"/>
  <text x="343" y="80" fill="#818CF8" font-family="{FONT_SANS}" font-size="18" font-weight="700">{public_repo_count} / {total_stars}</text>
  <text x="343" y="101" fill="#94A3B8" font-family="{FONT_SANS}" font-size="11">Repos / Stars</text>

  <text x="28" y="139" fill="#94A3B8" font-family="{FONT_SANS}" font-size="11" font-weight="600">
    Recent 28-Week Cadence
  </text>
  <text x="333" y="139" text-anchor="end" fill="#64748B" font-family="{FONT_SANS}" font-size="10">Less</text>
  {"".join(legend_swatches)}
  <text x="403" y="139" fill="#64748B" font-family="{FONT_SANS}" font-size="10">More</text>
  {"".join(heatmap_cells)}

  <!-- Right Panel: Languages & Focus -->
  <text x="472" y="38" fill="#F8FAFC" font-family="{FONT_SANS}" font-size="15" font-weight="700">
    Language Distribution &amp; Tracks
  </text>
  <text x="872" y="38" text-anchor="end" fill="#64748B" font-family="{FONT_SANS}" font-size="11">
    Synced {escape(updated_label)}
  </text>

  <text x="472" y="72" fill="#94A3B8" font-family="{FONT_SANS}" font-size="12">
    Public Owned Repositories · {total_prs} Pull Requests
  </text>
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5" fill="#1E293B"/>
  <g clip-path="url(#langBarClip)">
    {"".join(bar_segments)}
  </g>
  {"".join(legend_rows)}

  <text x="472" y="168" fill="#94A3B8" font-family="{FONT_SANS}" font-size="11" font-weight="600">
    CORE ENGINEERING TRACKS &amp; STACK
  </text>
  <rect x="472" y="178" width="126" height="28" rx="7" fill="#0F172A" stroke="#38BDF8" stroke-opacity="0.45"/>
  <text x="535" y="196" text-anchor="middle" fill="#38BDF8" font-family="{FONT_SANS}" font-size="11.5" font-weight="600">Local &amp; Mac AI</text>

  <rect x="609" y="178" width="126" height="28" rx="7" fill="#0F172A" stroke="#34D399" stroke-opacity="0.45"/>
  <text x="672" y="196" text-anchor="middle" fill="#34D399" font-family="{FONT_SANS}" font-size="11.5" font-weight="600">Agents &amp; RAG</text>

  <rect x="746" y="178" width="126" height="28" rx="7" fill="#0F172A" stroke="#818CF8" stroke-opacity="0.45"/>
  <text x="809" y="196" text-anchor="middle" fill="#818CF8" font-family="{FONT_SANS}" font-size="11.5" font-weight="600">MLOps &amp; Privacy</text>

  <rect x="472" y="214" width="126" height="28" rx="7" fill="#161B22" stroke="#30363D"/>
  <text x="535" y="232" text-anchor="middle" fill="#CBD5E1" font-family="{FONT_MONO}" font-size="10.5">Ollama / Node.js</text>

  <rect x="609" y="214" width="126" height="28" rx="7" fill="#161B22" stroke="#30363D"/>
  <text x="672" y="232" text-anchor="middle" fill="#CBD5E1" font-family="{FONT_MONO}" font-size="10.5">Fuzz / NLI / OCR</text>

  <rect x="746" y="214" width="126" height="28" rx="7" fill="#161B22" stroke="#30363D"/>
  <text x="809" y="232" text-anchor="middle" fill="#CBD5E1" font-family="{FONT_MONO}" font-size="10.5">ADWIN / PSI / DP</text>
</svg>
"""


def build_repo_card_svg(spec: dict[str, Any], repo_meta: dict[str, Any] | None) -> str:
    """Render a self-hosted 440x154 clickable repository showcase SVG card."""
    pl = (repo_meta or {}).get("primaryLanguage") or {"name": "Python", "color": "#3572A5"}
    lang_name = str(pl.get("name") or "Python")
    lang_color = str(pl.get("color") or "#3572A5")
    stars = int((repo_meta or {}).get("stargazerCount") or 0)
    forks = int((repo_meta or {}).get("forkCount") or 0)
    accent = str(spec["metric_color"])

    return f"""<svg width="440" height="154" viewBox="0 0 440 154" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="repoBg_{escape(spec['slug'])}" x1="0" y1="0" x2="440" y2="154" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0D1117"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
  </defs>
  <rect width="440" height="154" rx="12" fill="url(#repoBg_{escape(spec['slug'])})"/>
  <rect x="0.75" y="0.75" width="438.5" height="152.5" rx="11.25" stroke="#30363D" stroke-width="1.5"/>
  <rect x="0" y="16" width="3.5" height="32" rx="1.75" fill="{escape(accent)}"/>

  <!-- Top row: title + metric pill -->
  <text x="20" y="34" fill="#F8FAFC" font-family="{FONT_SANS}" font-size="15" font-weight="700">{escape(spec["title"])}</text>
  <rect x="278" y="16" width="144" height="24" rx="12" fill="#161B22" stroke="{escape(accent)}" stroke-opacity="0.5"/>
  <text x="350" y="32" text-anchor="middle" fill="{escape(accent)}" font-family="{FONT_SANS}" font-size="11" font-weight="600">{escape(spec["metric"])}</text>

  <!-- Two-line verified technical summary -->
  <text x="20" y="66" fill="#CBD5E1" font-family="{FONT_SANS}" font-size="12.5">{escape(spec["line1"])}</text>
  <text x="20" y="85" fill="#94A3B8" font-family="{FONT_SANS}" font-size="12.5">{escape(spec["line2"])}</text>

  <!-- Footer bar: language dot, repo owner/stats, domain tag -->
  <line x1="20" y1="112" x2="420" y2="112" stroke="#1E293B" stroke-width="1"/>
  <circle cx="25" cy="133" r="5" fill="{escape(lang_color)}"/>
  <text x="36" y="137" fill="#E2E8F0" font-family="{FONT_SANS}" font-size="11.5" font-weight="500">{escape(lang_name)}</text>
  <text x="156" y="137" fill="#94A3B8" font-family="{FONT_MONO}" font-size="11">★ {stars} · ⑂ {forks}</text>
  <text x="420" y="137" text-anchor="end" fill="#64748B" font-family="{FONT_SANS}" font-size="11">{escape(spec["tag"])}</text>
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GitHub profile SVG cards.")
    parser.add_argument("--username", default="Thush099")
    parser.add_argument("--output", default="assets/stats.svg")
    parser.add_argument("--cards-dir", default="assets/cards")
    parser.add_argument("--json-file", default=None, help="Optional cached GraphQL JSON file")
    args = parser.parse_args()

    if args.json_file:
        data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            raise RuntimeError("GITHUB_TOKEN or GH_TOKEN environment variable is required.")
        data = fetch_github_stats(args.username, token)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_stats_svg(data), encoding="utf-8")
    print(f"Generated {out_path}")

    user = data["data"].get("user") or data["data"]["viewer"]
    owned_by_name = {r["name"]: r for r in user["repositories"]["nodes"]}
    domain_ai = data["data"].get("domainAi")

    cards_dir = Path(args.cards_dir)
    cards_dir.mkdir(parents=True, exist_ok=True)
    for spec in FEATURED_SPECS:
        meta = domain_ai if spec["repo"] == "domain-ai" else owned_by_name.get(spec["repo"])
        card_path = cards_dir / f"{spec['slug']}.svg"
        card_path.write_text(build_repo_card_svg(spec, meta), encoding="utf-8")
        print(f"Generated {card_path}")


if __name__ == "__main__":
    main()
