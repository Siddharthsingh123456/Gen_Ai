Assignment 23 data folder

Set YOUTUBE_URL in your environment before running the YouTube tasks.

Example:
Windows PowerShell:
$env:YOUTUBE_URL="https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

The project deliberately does not use fake transcripts or fake retrieval results.
If the YouTube transcript, OpenAI API, or internet connection is unavailable,
the program reports the real error instead of pretending that the task succeeded.
