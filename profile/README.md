<p align="center">
  <img src="https://flyto2.com/logo.png" width="120" alt="Flyto" />
</p>

<h1 align="center">Flyto2</h1>

<p align="center">
  <b>Automate your browser once. Replay from any step. Never re-run the whole thing again.</b>
</p>

<p align="center">
  <a href="https://flyto2.com">🌐 Website</a> ·
  <a href="https://docs.flyto2.com">📖 Docs</a> ·
  <a href="https://www.youtube.com/@Flyto2">📺 YouTube</a> ·
  <a href="https://github.com/flytohub/flyto-core/discussions">💬 Discussions</a>
</p>

---

## Hi 👋 we're Flyto

We build two things:

### 🤖 Automation that doesn't fall apart when step 8 fails

> Opening browsers. Waiting for pages. Filling forms. Clicking. Screenshotting.
> Downloading reports. Pushing data into a sheet.
>
> Annoying once a week. Unacceptable thirty times a week.

The real pain isn't writing the script — it's that when step 8 fails, you re-run the whole thing. **We record every step and let you replay from any one of them.**

```bash
pip install flyto-core[browser] && playwright install chromium
flyto recipe competitor-intel --url https://github.com/pricing
```

```
  Step  1/12  browser.launch         ✓      420ms
  Step  2/12  browser.goto           ✓    1,203ms
  Step  3/12  browser.screenshot     ✓    1,847ms  → saved intel-desktop.png
  Step  8/12  browser.performance    ✗      ERROR
  
  # next run only touches step 8 onwards
  flyto replay --from-step 8
```

### 🧠 Turn your chaos pile into a knowledge workspace

> How many "I'll read this later" PDFs are on your laptop?
> How many "I'm scared to touch this" folders on your NAS?
> How many "I wrote this somewhere in Notion" pages that you can't find?

We don't force you to organise. You drop things in an Inbox. The engine reads, classifies, links. When a topic has enough gravity, it **suggests** you promote it into a Project. You never had to decide upfront.

**Core rule: we never touch your original files.** Your NAS layout stays exactly the way it was. We index, cache, and map — we don't move bytes around.

---

## 🌟 Flagship products

### [flyto-core](https://github.com/flytohub/flyto-core)

> **A debuggable automation engine.** Trace every step. Replay from any point.

Python + Playwright under the hood. Workflows are YAML. Every step emits a trace so failures aren't a black box. Built for:

- Competitor monitoring, price tracking, market intel
- Repetitive data extraction and shaping
- RPA that needs to be stable, debuggable, collaboratively owned

```yaml
id: competitor_intel_v1
steps:
  - id: launch
    module: browser.launch
    params: { stealth: true, headless: true }
  - id: goto
    module: browser.goto
    params: { url: "{{target_url}}", wait_until: networkidle }
  - id: snap
    module: browser.screenshot
    params: { path: "intel-{{date}}.png" }
  # every step replayable in isolation
```

📦 `pip install flyto-core`
⭐ [Star on GitHub →](https://github.com/flytohub/flyto-core)

### [flyto-cloud](https://cloud.flyto2.com) — Flyto Automation

> **Workflow automation SaaS + desktop app.** Ship real work, not prototypes.

The polished surface over flyto-core. Not a toy, not a beta:

- 🎨 Drag-and-drop workflow canvas — no YAML required to ship something useful
- 🏪 Template Marketplace — run someone else's workflow, or publish your own
- 🖥️ Tauri desktop build — passwords and data stay on your machine
- 👥 Team features — shared workflows, schedules, queues, full audit log

🌐 [cloud.flyto2.com](https://cloud.flyto2.com) · [desktop download](https://flyto2.com/app.html)

---

## 🧰 The rest of the garden

| Repo | What it is |
|------|------------|
| [flyto-cortex](https://github.com/flytohub/flyto-cortex) | Knowledge workspace frontend (React 19 + Mantine) |
| [flyto-engine](https://github.com/flytohub/flyto-engine) | Go backend shared by Cortex (and soon Cloud) |
| [flyto-plugins-js](https://github.com/flytohub/flyto-plugins-js) | Browser plugins / module packs |
| [flyto-indexer](https://github.com/flytohub/flyto-indexer) | Code-intelligence MCP server |
| [flyto-docs](https://github.com/flytohub/flyto-docs) | All-product documentation |
| [flyto-i18n](https://github.com/flytohub/flyto-i18n) | Shared translations |

---

## 💡 What we care about

**1. Traceability over magic.**
Every step records what it did. When an AI-generated script blows up, you can see which step, why, and whether it's safe to continue from there.

**2. Your data stays yours.**
flyto-core desktop mode runs offline by default. The knowledge workspace never rewrites your NAS / Drive. We index, cache, and overlay — the originals are untouched.

**3. Code that runs today.**
No "coming soon". Every repo has a working `pip install` / `npm install` / `go build` path. Open it and try it.

**4. Open source, seriously.**
- ✅ Thousands of tests (flyto-cloud: 1,730+; flyto-engine: every core package covered)
- ✅ Real CI/CD with automated deployment
- ✅ Security engineering — hash-chained audit logs, permission matrix, idempotency keys, typed error envelopes
- ✅ Ops-grade docs (API reference, data model, operations runbook)

---

## 🚀 Try it

**Command line (30 seconds):**
```bash
pip install flyto-core[browser] && playwright install chromium
flyto recipe competitor-intel --url https://github.com/pricing
```

**Web app:**
👉 [cloud.flyto2.com](https://cloud.flyto2.com)

**Desktop (works offline):**
👉 [flyto2.com/app.html](https://flyto2.com/app.html)

---

## 🤝 Contributing

PRs welcome. Pick a [good first issue](https://github.com/flytohub/flyto-core/contribute), or drop by [Discussions](https://github.com/flytohub/flyto-core/discussions) and tell us what you want to build.

We usually respond to issues and PRs within 24 hours.

---

## 📬 Contact

- 💬 [GitHub Discussions](https://github.com/flytohub/flyto-core/discussions) — community Q&A
- 📖 [docs.flyto2.com](https://docs.flyto2.com) — full documentation
- 📺 [YouTube @Flyto2](https://www.youtube.com/@Flyto2) — demos and walkthroughs
- 📧 hello@flyto2.com — partnerships, enterprise, press

---

<p align="center">
  <sub>Made with ☕ in Taiwan. MIT licensed unless stated otherwise.</sub>
</p>
