import urllib
from urllib import request
from urllib.parse import parse_qs
import sys


# THE BASIC IDEA OF PARSING YOUTUBE VIDEOS,
# WITHOUT COMPLETE EXCEPTION HANDLING

# V2:
# Add non-English support.
# fix video name containing '/' problem.


def get_vid(resp):
    data = resp.read().decode('utf-8')

    info = parse_qs(data)
    try:
        title = info["title"][0]
    except KeyError:
        print("Sorry, this video is not allowed to be downloaded from youtube.")
        try:
            reason = info["reason"][0]
            print("Blocked reason: " + reason)
        except:
            pass
        return -1
    # check if video title is legal
    if '/' in title:
        title = title.replace('/', '-')

    v_title = title + ".mp4"
    print("title: " + v_title + "\n")
    stream_map = info["url_encoded_fmt_stream_map"][0]
    v_info = stream_map.split(",")
    res_level = len(v_info)

    try:
        print("Please select the resolution level of the video, ")
        resolution = int(
            input("1 - %d, highest to lowest, q to quit: " % (res_level,)))
    except ValueError:
        return 1

    while 1 > resolution > res_level:
        print("Please enter the right number.")
        resolution = int(
            input("Please select the resolution of the video( 1-" + str(res_level) + ", highest to lowest): "))
    resolution -= 1  # get the index

    video = v_info[resolution]
    item = parse_qs(video)
    url = item["url"][0]
    resp = request.urlopen(url)
    tot_size = resp.headers["Content-Length"]
    buff = resp.read(1024)
    done = 0
    fp = open("tmp/" + v_title, "wb+")
    while buff:
        fp.write(buff)
        done += 1024
        perct = done / float(tot_size) * 100.0
        buff = resp.read(1024)

        # display the progress bar
        sys.stdout.write(("=" * int(perct / 5)) + ("" * (20 - int(perct / 10))) + ("\r [ %3.2f" % perct + "% ] "))
        sys.stdout.flush()
    fp.close()
    return 0


if __name__ == "__main__":
    v_id = input("Id of the video: ")
    v_url = "https://www.youtube.com/get_video_info?video_id=" + v_id
    try:
        resp = request.urlopen(v_url)
    except urllib.error.HTTPError as e:
        print("Cannot open the page.")
        print(e.code)
        raise (e)
    ok = get_vid(resp)
    if ok == 0:
        print("Finish downloading.")
    elif ok == -1:
        print("Downloading failed.")
    elif ok == 1:
        print("Byebye")
