# javar-skills

Personal Claude Code skill collection.

## Skills

### youtube-summarizer

Summarizes YouTube videos by fetching their transcripts.

- Paste any YouTube URL and Claude will fetch the transcript and produce a structured summary
- Language priority: English → Russian → whatever's available
- Output: TL;DR, Key Points, and Details sections

**Requires:** `pip install youtube-transcript-api`

## Installation

```bash
claude plugins install ivliag/javar-skills
```

Or clone and use as a local plugin:

```bash
git clone https://github.com/ivliag/javar-skills ~/.claude/plugins/javar-skills
```

Then add to `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "javar-skills@local": true
  }
}
```
