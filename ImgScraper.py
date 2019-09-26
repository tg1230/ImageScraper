import os
import urllib.request

# takes in a single line of js which holds the link to the photos
# a script can be written to grap the link or this can be modified further to do that as needed

def parse_link(js_line, link_dir, img_dir):
    # parse link while there is still an http link
    index = js_line.find('http')
    file_num = str()
    while index != -1:
        parsed_link = ""
        # start from the first instance of http found and create link
        for char in js_line[index:]:
            index += 1
            # end at links closing quotes
            if char == '"':
                # cut off first link, start search again
                js_line = js_line[index:]
                index = js_line.find('http')
                break
            else:
                # building link
                parsed_link += char
        # save img with the http link and text_file name
        file_num += "x"
        save_image(parsed_link, link_dir, img_dir, file_num)
    return


def save_image(parsed_link, link_dir, img_dir, file_num):

    # get file name and complete path
    file_name = os.path.basename(link_dir).split('.')
    complete_path = os.path.join(img_dir + file_name[0], file_name[0] + file_num + ".jpg")

    # retrieve img
    try:
        img = urllib.request.urlopen(parsed_link)
    # else put link to image in file
    except:
        with open(complete_path, 'wb') as f:
            f.write(parsed_link)
        return

    complete_path = os.path.join(img_dir + file_name[0], file_name[0] + file_num + ".jpg")
    with open(complete_path, 'wb') as f:
        f.write(img.read())


def parse_and_download():
    # create a folder with these subdirectories
    link_dir = os.getcwd() + "/ImageScraper/Links"
    img_dir = os.getcwd() + "/ImageScraper/Images/"

    # need to traverse Links directory and open each file
    for root, dirs, files in os.walk(link_dir):
        for txt_file in files:
            # hardcoding for "optimization"
            link_dir = "/Users/travisgarcia/ImageScraper/Links"
            link_dir = os.path.join(link_dir, txt_file)
            img_dir = "/Users/travisgarcia/ImageScraper/Images/"
            # open and read first line
            if link_dir.endswith(".txt"):
                #  encoding issue with html
                with open(link_dir, encoding='utf-16') as f:
                    for js_line in f:
                        # parse js line and save photo
                        parse_link(js_line, link_dir, img_dir)
