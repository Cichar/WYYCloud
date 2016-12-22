from selenium import webdriver
import time
import csv
import os
import threading
import queue

q = queue.Queue()
lock = threading.Lock()
rightMusicList = {}

def getPlayListId(pagenum,musicStyle):
    driver = webdriver.PhantomJS()
    #歌单列表URL规则，offset=后面接页码，从0开始，以35为基数递增
    base_url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%s&limit=35&offset=' % musicStyle
    driver.get(base_url + str(pagenum))     
    driver.switch_to_frame('g_iframe')      #进入iframe
    id = driver.find_elements_by_xpath('//a[@data-res-id]') #定位歌单ID
    playListId = []
    for i in id:
        playListId.append(i.get_attribute('data-res-id'))
    driver.quit()    
    return playListId

def getMusic(playListId):
    global rightMusicList
    global findedMusic
    driver = webdriver.PhantomJS()
    base_url = 'http://music.163.com/#/playlist?id='
    #获取传入歌单中的歌曲ID
    driver = webdriver.PhantomJS()
    driver.get(base_url+str(playListId))
    driver.switch_to_frame('g_iframe')
    ids = driver.find_elements_by_css_selector('a[href^=\/song]')
    for id in ids:
        mid = id.get_attribute('href')[29:]
        q.put(mid)
    driver.quit()
    ths = []
    try:
        for i in range(3):
            t = threading.Thread(target = compareMusic)
            t.deamon = True
            t.start()
            ths.append(t)
        for th in ths:
            th.join()
    except Exception as e:
        pass

def compareMusic():
    global rightMusicList
    driver = webdriver.PhantomJS()
    base_url = 'http://music.163.com/#/song?id='
    while not q.empty():
        musicId = q.get()
        driver.get(base_url+str(musicId))
        driver.switch_to_frame('g_iframe')
        time.sleep(0.3) #等待0.2秒，加载数据
        flags = driver.find_elements_by_xpath('//*[@id="cnt_comment_count"]')
        for flag in flags:
            try:
                lock.acquire()
                if int(flag.text) >= 10000:
                    print('验证歌曲ID：'+str(musicId)+',评论数：'+str(flag.text)+'>=10000,符合条件,写入文件')
                    csvFile = open('F:\Myspiders\WYYCloud\music.csv','a',newline='') #csv文件在要存储的地方创建
                    writer = csv.writer(csvFile)
                    writer.writerow((musicId,flag.text))
                    csvFile.close()
                else:
                    print('验证歌曲ID：'+str(musicId)+',评论数：'+str(flag.text)+'<10000,不符合条件.')
            except ValueError:
                print('无法验证歌曲ID：'+str(musicId)+'继续验证下一首')
            finally:
                lock.release()
                q.task_done()
    driver.quit()        
    print('歌曲执行完毕，即将切换下一份歌单..')
    print('-----------------------------------')
    
def findmusic(pages,musicStyle):  
    for i in range(pages):
        pagenum = i*35      #计算num
        playListIds = getPlayListId(pagenum,musicStyle)    #获取歌单ID
        for playListId in playListIds:
            print('正在第%s页的歌单%s中获取符合规则的歌曲..' % (i+1,playListId))
            musics = getMusic(playListId)       #获取符合规则的music
            
if __name__ == '__main__':
    findmusic(42,'%E7%94%B5%E5%AD%90')  #'%E7%94%B5%E5%AD%90' 是电子这个主题的代码。其他风格相应替换
