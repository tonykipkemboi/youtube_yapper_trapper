#!/usr/bin/env python
from youtube_yapper_trapper.crew import YoutubeCommentsCrew
from dotenv import load_dotenv
import agentops

load_dotenv()
agentops.init()


def extract_video_id(url):
    import re

    # This regex will match the video ID from any YouTube URL (normal, shortened, embedded)
    try:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        return match.group(1) if match else None
    except Exception as e:
        print(e)


def run():
    video_id = extract_video_id(input("🚀 Enter YouTube URL: "))
    if not video_id:
        print("🚨 Invalid YouTube URL provided.")
        return

    inputs = {"video_id": video_id}
    crew = YoutubeCommentsCrew()
    result = crew.crew().kickoff(inputs=inputs)
    print("Analysis Result:")
    print(result)


if __name__ == "__main__":
    run()
