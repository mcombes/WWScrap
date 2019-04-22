import urllib.request as urlRequest
import urllib.parse as urlParse
import sys
import codecs as cs
import os

def MakeAChapter(page):
    return page.split('class="fr-view">')[1].splitlines()[1]

def MakeAWebpage(pathname, meme=True, default=""):
    chapterName = pathname.split("/")[-1]
    bookName = pathname.split("/")[-2]
    file_name = chapterName+'.html'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    req = urlRequest.Request(pathname, headers = headers)
    x = urlRequest.urlopen(req)
    sourceCode = x.read()
    try:
        os.makedirs("htmlCache")
    except OSError:
        if not os.path.isdir("htmlCache"):
            raise
    if(meme):
        html = cs.open("htmlCache/"+file_name,'w','utf-8')
        decoded=sourceCode.decode("utf-8") 
        html.write(MakeAChapter(decoded))
        html.close()
    else:
        html = cs.open("htmlCache/"+default,'w','utf-8')
        decoded=sourceCode.decode("utf-8") 
        html.write(decoded)
        html.close()
            
def GatherCompleteSummaryPages():
    MakeAWebpage("https://www.wuxiaworld.com/" + "/".join(sys.argv[1].split("/")[-2:]),False,"index.html")
    memeFile=open("htmlCache/index.html","r",encoding="utf-8")
    wholeIndex=memeFile.read()
    memeFile.close()
    ListeLiens=[]
    mymeme = wholeIndex.split("panel-body")[1].split('id="sidebar"')[0]
    xd=mymeme.splitlines()
    for line in xd:
        if line.count("a href")!=0:
            ListeLiens.append(line.split('"')[1])
    return(ListeLiens)
    
def WriteSummary(listeLiens, outPath="htmlCache/toc.html"):
    html_doc = """
<html>
   <body>
     <h1>Table of Contents</h1>
     <p style="text-indent:0pt">

     """
    for lien in listeLiens:
        MakeAWebpage("https://www.wuxiaworld.com"+lien)
        chapterName = ("https://www.wuxiaworld.com/"+lien).split("/")[-1]
        html_doc = html_doc + "<a href=" + "\"" + chapterName + ".html\">" + chapterName + "</a><br/>" + "\r\n"
    html_doc += """
     </p>
   </body>
</html>
    """
    tocHTML = cs.open(outPath, 'w', 'utf-8')
    tocHTML.write(html_doc)
    tocHTML.close()
maListe=GatherCompleteSummaryPages()
WriteSummary(maListe)