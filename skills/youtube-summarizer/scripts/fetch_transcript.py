#!/usr/bin/env python3
"""
Fetch transcript from a YouTube video.
Prefers English, falls back to Russian, then any available language.

Usage: python fetch_transcript.py <youtube_url_or_video_id>
"""

import sys
import re


def extract_video_id(url_or_id):
    """Extract video ID from a YouTube URL or return the ID as-is."""
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id.strip()


def fetch_transcript(video_id):
    """
    Fetch transcript for a video, preferring English then Russian.
    Returns (transcript_text, language_code).
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()

    # Priority: English variants, then Russian, then anything
    language_priority = ["en", "en-US", "en-GB", "ru"]

    try:
        transcript_list = api.list(video_id)
    except Exception as e:
        print(f"Error fetching transcript list: {e}", file=sys.stderr)
        sys.exit(1)

    # Build a map of available transcripts by language code
    available = {}
    for t in transcript_list:
        available[t.language_code] = t

    chosen = None
    lang_used = None

    for lang in language_priority:
        if lang in available:
            chosen = available[lang]
            lang_used = lang
            break

    # Fall back to first available
    if chosen is None:
        all_transcripts = list(available.values())
        if not all_transcripts:
            print("Error: No transcripts available for this video.", file=sys.stderr)
            sys.exit(1)
        chosen = all_transcripts[0]
        lang_used = chosen.language_code

    try:
        entries = chosen.fetch()
        text = " ".join(entry.text for entry in entries)
        return text, lang_used
    except Exception as e:
        print(f"Error fetching transcript content: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_transcript.py <youtube_url_or_video_id>", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[1]
    video_id = extract_video_id(raw)

    text, lang = fetch_transcript(video_id)

    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", prefix=f"yt_{video_id}_", delete=False
    )
    tmp.write(f"[language: {lang}]\n")
    tmp.write(text)
    tmp.close()

    print(tmp.name)


if __name__ == "__main__":
    main()
