from threading import Thread

from requests import session
from datetime import datetime
from os import makedirs  , path


MAX_TRY = 5
def down_load(url , url_index , retry = 0):
    if retry >= MAX_TRY:
        with open('error.txt' , 'a') as f:
            f.write(f'{url}\n')
            
    output_folder  = datetime.today().strftime("%Y-%m-%d")
    makedirs(output_folder , exist_ok = True)
    try:
        with session() as s:
            resp = s.get(url)
            file_name = f'{url_index}.mp4'
            with open(f'{output_folder}/{file_name}' , 'wb') as f:
                f.write(resp.content)
        print(f'{url} downloaded successfully as {file_name}')
    except Exception as e:
        return down_load(url , url_index , retry + 1)

links = open('douyin-video-links.txt' , 'r' , encoding = 'utf-8').read().splitlines()
thread_count = 10
for i in range(0,len(links) , thread_count):
    threads = []
    batch = links[i:i+thread_count]
    for link in batch:
        t = Thread(target = down_load , args = (link , links.index(link)))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()