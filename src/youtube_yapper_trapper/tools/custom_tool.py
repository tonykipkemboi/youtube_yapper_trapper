from crewai_tools import BaseTool
import requests
import os


class YouTubeCommentsTool(BaseTool):
    name: str = "YouTube Comments Fetcher"
    description: str = "Fetches all comments from a specified YouTube video URL using the YouTube Data API."

    # https://www.youtube.com/watch?v=sNa_uiqSlJo

    #print(f'vedio ID: yaya')

    def _run(self, video_id: str) -> list:
        comments = []
        page_token = ""
        base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
        headers = {"Accept": "application/json"}

        #print(f'vedio ID: {video_id}')

        try:
            self.validate_video_id(video_id)
            # print(f'validate: {validate_video_id}')
        except ValueError as e:
            return f"Error: {str(e)}"

        #print(f'vedio ID: {video_id}')

        while True:
            params = {
                "key": os.environ["YOUTUBE_API_KEY"],
                "part": "snippet",
                "videoId": video_id,
                "maxResults": 100,
                "pageToken": page_token,
                "textFormat": "plainText",
            }
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    comment = item["snippet"]["topLevelComment"]["snippet"][
                        "textDisplay"
                    ]
                    comments.append(comment)
                page_token = data.get("nextPageToken")
                if not page_token:
                    break
            else:
                self.handle_api_error(response)

        return comments

    def validate_video_id(self, video_id):
        """Validate the video ID by checking its availability."""
        response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=id&id={
                                video_id}&key={os.getenv('YOUTUBE_API_KEY')}")
        if response.json().get("pageInfo", {}).get("totalResults", 0) == 0:
            raise ValueError("Video ID not valid or video is not accessible.")

    def handle_api_error(self, response):
        """Handle common API errors based on response status code."""
        if response.status_code == 403:
            error_details = response.json()
            if "error" in error_details:
                if "errors" in error_details["error"]:
                    for error in error_details["error"]["errors"]:
                        if error.get("reason") == "commentsDisabled":
                            raise Exception("Comments are disabled for this video.")
                        elif error.get("reason") == "forbidden":
                            raise Exception(
                                "Insufficient permissions to access the comments."
                            )
        elif response.status_code == 404:
            error_details = response.json()
            if "error" in error_details:
                if "errors" in error_details["error"]:
                    for error in error_details["error"]["errors"]:
                        if error.get("reason") == "private":
                            raise Exception("The specified video ID is Pivate.")
                        elif error.get("reason") == "restricted":
                            raise Exception("The specified channel ID is restrictedwas not found.")
        elif response.status_code == 401:
            error_details = response.json()
            if "error" in error_details:
                if "errors" in error_details["error"]:
                    for error in error_details["error"]["errors"]:
                        if error.get("reason") == "videoNotFound":
                            raise Exception("The specified video ID was not found.")
                        elif error.get("reason") == "channelNotFound":
                            raise Exception("The specified channel ID was not found.")
        else:
            response.raise_for_status()  # Raise any other HTTP errors as exceptions
