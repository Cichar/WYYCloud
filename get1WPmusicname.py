from selenium import webdriver
import time
import csv
import os

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
    driver = webdriver.PhantomJS()
    base_url = 'http://music.163.com/#/playlist?id='
    #获取传入歌单中的歌曲ID
    driver = webdriver.PhantomJS()
    driver.get(base_url+str(playListId))
    driver.switch_to_frame('g_iframe')
    ids = driver.find_elements_by_css_selector('a[href^=\/song]')
    musicIdList = []
    for id in ids:
        musicIdList.append(id.get_attribute('href')[29:])
    driver.quit()
    return compareMusic(musicIdList)

def compareMusic(musicIdList):
    driver = webdriver.PhantomJS()
    base_url = 'http://music.163.com/#/song?id='
    rightMusicList = {}
    for musicId in musicIdList:
        driver.get(base_url+str(musicId))
        driver.switch_to_frame('g_iframe')
        time.sleep(0.5) #等待0.5秒，加载数据
        flags = driver.find_elements_by_xpath('//*[@id="cnt_comment_count"]')
        for flag in flags:
            if int(flag.text) >= 10000:
                print('验证歌曲ID：'+str(musicId)+',评论数：'+str(flag.text)+'>=10000,符合条件.')
                rightMusicList[musicId] = flag.text
            else:
                print('验证歌曲ID：'+str(musicId)+',评论数：'+str(flag.text)+'<10000,不符合条件.')
    driver.quit()
    if len(rightMusicList) > 0:
        print('存在符合规则的歌曲，写入中..')
        csvFile = open('D:\Python练习\爬虫项目\爬取网易云歌单\music.csv','a',newline='') #csv文件在要存储的地方创建
        writer = csv.writer(csvFile)
        try:
            for music in rightMusicList:
                writer.writerow((music,rightMusicList[music]))
        finally:
            csvFile.close()
        print('歌曲写入完毕，即将切换下一份歌单..')
    else:
        print('不存在符合规则的歌曲，即将切换下一份歌单')
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
