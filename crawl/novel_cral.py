import urllib.request as req
import bs4
import json
import collections
from collections import Counter

#進入某頁並回傳下頁url
def crawl(url,names,node):
    #建立一個Request物件，附加request haders 的資訊
    #模擬request
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })

    #攔截response
    #透過urlpopen開啟網頁
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    """
    with ... as ...
    response=req.urlopen(request)#連接成功後回傳的
    data=response.read().decode("utf-8")#將回傳的內容解碼
    結束、處理例外
    """
    #print(data)
    #解析原始碼
    root=bs4.BeautifulSoup(data,"html.parser")
    #這裡的root就是解析完成後，所產生的結構樹物件，接下來所有資料的搜尋、萃取等操作都會透過這個物件來進行。
    #html.parser 為python內建的解析器，lxml為解析速度最快的
    all_title = root.find("div",class_="mulu-list")
    titles=all_title.find_all("li")
    n=0;
    diction = []
    diction_tiems = []
    with open('connect.json', 'w', encoding='utf-8') as f:
        new_nodes = []
        #print(node)
        for i in range(len(node)):
            node_dic = collections.OrderedDict()
            node_dic["id"] = node[i]["id"]
            node_dic["group"] = 0
            node_dic["times"] = 0
            new_nodes.append(node_dic)
        #print(new_nodes[0])
        for title in titles:
            print(n)
            if title.a != None:#如果標題包含 a標籤(沒有被刪除)
                link=title.a["href"]
                diction+=crawl_text(link,names,new_nodes)#進入此文章
                #print(diction)
            n=n+1
            #if(n>3) : break
        co =0
        while(co<len(new_nodes)):
            #print(new_nodes[co]['group'])
            if (new_nodes[co]['group']==0) :
                #print("is 0")
                del new_nodes[co]
            elif(new_nodes[co]['group']>100) :
                new_nodes[co]['group']=20
                new_nodes[co]['color']='rgba(255, 153, 51,1.0)'
                co=co+1
            elif(new_nodes[co]['group']>60) :
                new_nodes[co]['group']=15
                new_nodes[co]['color']='rgba(252, 197, 68,0.85)'
                co=co+1
            elif(new_nodes[co]['group']>30) :
                new_nodes[co]['group']=10
                new_nodes[co]['color']='rgba(252, 218, 68,0.75)'
                co=co+1
            elif(new_nodes[co]['group']>15) :
                new_nodes[co]['group']=8
                new_nodes[co]['color']='rgba(247, 229, 106,0.7)'
                co=co+1
            elif(new_nodes[co]['group']>8) :
                new_nodes[co]['group']=5
                new_nodes[co]['color']='rgba(250, 238, 127,0.65)'
                co=co+1
            elif(new_nodes[co]['group']>3) :
                new_nodes[co]['group']=3
                new_nodes[co]['color']='rgba(255, 247, 156,0.6)'
                co=co+1
            else:
                new_nodes[co]['group']=1
                new_nodes[co]['color']='rgba(255, 225, 255,0.55)'
                co=co+1
        json.dump(diction,f,ensure_ascii=False,sort_keys=False, indent=4);
        L = len(diction)
        #print(new_nodes)
        #c = [json.dumps(diction[k]) for k in range(L)]
        #print(diction[0])
        c = [str(diction[k]) for k in range(L)]
        with open('node_and_link.json', 'w', encoding='utf-8') as fp:
            #print(c)
            b = Counter(c)
            #print(b)
            #print("b:")
            #print(type(b))
            b_len = len(b)
            #print(len(b))
            e=json.dumps(b,ensure_ascii=False)
            #print(e)
            #print("________________________________")
            #print(type(e))
            for k in range(b_len) :
                #print(b.item())
                #print([key for key,value in b.items()][k])
                split_block = [key for key,value in b.items()][k].split('\'')
                #first = split_block[3]
                #print(first)
                s = split_block[3]
                t = split_block[7]
                #print(s)
                #print(t)
                #print([value for key,value in b.items()][k])
                dic = collections.OrderedDict()
                dic["source"] = s;
                dic["target"] = t;
                if([value for key,value in b.items()][k]>60) :
                    dic["value"] = 12;
                else : dic["value"] = round([value for key,value in b.items()][k]/5,2);
                diction_tiems.append(dic)
            final = {"nodes":new_nodes,"links":diction_tiems}
            #print(final)"group"
            json.dump(final,fp,ensure_ascii=False,sort_keys=False, indent=4);
#爬文章內容
def crawl_text(url,names,new_nodes):
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")
    content = root.find("div",class_="neirong")
    parts = content.text.split('。')

    #N = len(names)
    N = len(new_nodes)
    #with open('connect.json', 'w', encoding='utf-8') as f:
    diction = []

    for part in parts:
        #print("part : "+part)
        cross = []
        k_save=[]
        for k in range(N):
            #if(names[k] in part) :
            if(new_nodes[k]["id"] in part) :
                #print(names[k])
                #cross.append(names[k])
                cross.append(new_nodes[k]["id"])
                k_save.append(k)
                new_nodes[k]["times"] = new_nodes[k]["times"]+1
                #new_nodes[k]["group"] = new_nodes[k]["group"]+1
        if(len(cross)>=2):
            for a in range(len(k_save)):
                new_nodes[k_save[a]]["group"] = new_nodes[k_save[a]]["group"]+1
            for i in range(len(cross)):
                for j in range(i+1,len(cross)):
                    #print(cross)
                    #print(cross[i]," ",cross[j])
                    dic = collections.OrderedDict()
                    dic["source"] = cross[i];
                    dic["target"] = cross[j];

                    #dic["value"] = 1;
                    d=dict(dic)
                    diction.append(d)
    return diction
        #json.dump(d,f,ensure_ascii=False,sort_keys=False, indent=4);
url="https://www.51shucheng.net/zh-tw/wuxia/yitiantulongji"
file = 'character.json'
with open(file, 'r',encoding="utf-8") as obj:
    data = json.load(obj)
N=len(data['nodes'])
#print(N)
names = [(data['nodes'][k]['id']) for k in range(N)]
#print(names)
#print(data['nodes'])
crawl(url,names,data['nodes'])
