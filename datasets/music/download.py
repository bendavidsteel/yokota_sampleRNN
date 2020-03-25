import json
import os
import youtube_dl

def get_filename(name):
    return "".join([c for c in name if c.isalpha() or c.isdigit() or c=='_']).rstrip()

def delete_all_with_extension(extension):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files_in_dir = os.listdir(dir_path)

    for item in files_in_dir:
        if item.endswith(extension):
            os.remove(os.path.join(dir_path, item))

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))

    links_path = dir_path + "/links.json"
    with open(links_path) as f:
        links_data = json.load(f)

    for artist in links_data["names"]:

        artist_name = artist["name"]

        for video_data in artist["links"]["full"]:

            album_name = video_data["name"]
            video_link = video_data["link"]

            output_file = os.path.join(dir_path, get_filename(artist_name + "_" + album_name))
            
            video_dl_command = "youtube-dl -o {}.webm {}".format(output_file, video_link)
            os.system(video_dl_command)

            audio_convert_command = "ffmpeg -i {}.webm {}.wav".format(output_file, output_file)
            os.system(audio_convert_command)

            # clean up unneeded video files
            delete_all_with_extension(".webm")


