---
name: youtube-summarizer
description: Summarize YouTube videos by fetching their subtitles/transcripts and producing a concise summary. Use this skill whenever the user shares a YouTube URL, video ID, or asks to summarize/recap/describe a YouTube video — even if they just paste a link without saying "summarize". Trigger on any youtube.com or youtu.be URL.
---

# YouTube Video Summarizer

Fetch the transcript of a YouTube video and summarize its content.

## Steps

### 1. Install dependency (if needed)

```bash
pip install youtube-transcript-api -q
```

### 2. Fetch the transcript

Run the helper script, which writes the transcript to a temp file and prints its path:

```bash
python <skill-dir>/scripts/fetch_transcript.py <video_url_or_id>
```

Then read the entire file in **one Bash call** using `cat`:

```bash
cat <path-printed-above>
```

This avoids chunked reads that require repeated approvals. The script tries languages in this order: **English first** (including auto-generated `en`), then **Russian** (`ru`), then whatever is available.

If the script fails (no transcript available, video is private, etc.), tell the user clearly what went wrong.

### 3. Summarize

Once you have the transcript text, produce a summary with these sections:

**Format:**
```
## Summary: [Video Title if known]

**TL;DR:** One or two sentences capturing the core message.

**Key Points:**
- ...
- ...
- ...

**Details:**
A few paragraphs covering the main ideas, arguments, or narrative in the video. Be faithful to the content — don't add opinions or facts not present in the transcript.
```

- Match the language of your summary to the transcript language (English transcript → English summary; Russian transcript → Russian summary).
- For short videos (< 5 min), the Details section can be brief or omitted.
- For long videos (> 30 min), include a timestamp-based breakdown if the transcript has timing data.
- Don't pad the summary — be concise and useful.
