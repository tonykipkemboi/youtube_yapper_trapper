#!/usr/bin/env python
from datetime import datetime
from youtube_yapper_trapper.crew import YoutubeCommentsCrew
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import agentops

load_dotenv()
#agentops.init()


def extract_video_id(url):
    import re
    # This regex will match the video ID from any YouTube URL (normal, shortened, embedded)
    try:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        return match.group(1) if match else None
    except Exception as e:
        print(e)


def run():
    inURL = input("🚀 Enter YouTube URL: ")
    video_id = extract_video_id(inURL)
    # video_id = extract_video_id(input("🚀 Enter YouTube URL: "))
    if not video_id:
        print("🚨 Invalid YouTube URL provided.")
        return

    # print(video_id)
    video_id = str (video_id)
    # print(video_id) https://youtu.be/4ZlK55_44II?si=XJRqaNPCa7FJovFz

    inputs = {"video_id": video_id, "url": inURL}
    crew = YoutubeCommentsCrew()
    result = crew.crew().kickoff(inputs=inputs)
    print("Analysis Result:")
    print(result) #.encode("utf-8"))
    
    
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the date and time in a specific format, e.g., YYYY-MM-DD_HH-MM
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")
    # Use the formatted date and time in the filename
    filename = f"Report_{formatted_datetime}.md"

    # print(f"Writing to {filename}") # Check the path where the file is being written

    # Open a new file with the dynamic filename in write mode
    with open(filename, 'w', encoding='utf-8') as file:
        # Write the Markdown content to the file
        file.write(result)
        file.flush()  # Ensure data is written to the disk

if __name__ == "__main__":
    run()
