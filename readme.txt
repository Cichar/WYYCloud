该爬虫用来爬取网易云音乐《电子》歌单中的过万评的16年电音曲目
某一风格歌单列表格式：'http://music.163.com/#/discover/playlist/?order=hot&cat=%E7%94%B5%E5%AD%90&limit=35&offset='
cat后面的%E7%94%B5%E5%AD%90，是电子这一风格的代码。寻找其他风格把这个替换掉就可以。
单份歌单格式：'http://music.163.com/#/playlist?id='
单首歌曲格式：'http://music.163.com/#/song?id='
歌单列表URL规则，offset=后面接页码，从0开始，以35为基数递增
csv文件在要存储的地方创建，同时该爬虫对于爬取的数据没有进行数据去重。
如要使用，请注明出处..
