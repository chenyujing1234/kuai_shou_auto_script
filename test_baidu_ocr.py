
# coding: utf-8

# In[2]:


# encoding:utf-8
import requests 
import requests
import base64

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=9M92Xoucd01BO6MxtyALGoNS&client_secret=OEKte7F4z9jNyDkmKkduEIA80iKNaE5o'
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"

response = requests.get(host)
if response:
    print(response.json())
access_token = response.json()["access_token"]


# In[2]:


# encoding:utf-8
# 获取图片OCR的结果 
def get_ocr_result(img_path):
    global access_token, request_url
    # 二进制方式打开图片文件
    #f = open('C:/Users/chenyujing/Documents/雷电模拟器/Pictures/Screenshots/Screenshot_2022-07-27-15-00-37.png', 'rb')
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        #print (response.json())
        try:
            json_return = response.json()
        except:
            print("!!!!!出现异常，response:{}".format(response))
            return None
        return json_return
    return None


# In[4]:


#img_path = "C:/Users/chenyujing/Desktop/AI爬虫/示例图片/Screenshot_20220725-221046.png"
img_path = "./评论.png"
json_result = get_ocr_result(img_path)
json_result


# In[5]:


def is_Chinese_chr(ch):
    if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def is_Chinese_str(str):
    for ch in str:
        if True == is_Chinese_chr(ch):
            return True
    return False


# In[7]:


def get_ping_lun_ocr_result(img_path):
    json_result = get_ocr_result(img_path)
    ping_lun_list = []
    for word_result in json_result["words_result"]:
        words = word_result["words"]
        location = word_result["location"]
        if "暂无评论" in words or "暂时没有更多" in words:
            return False, ping_lun_list
        # 条件1：不是明显出错的评论
        if True == words.startswith("昨天") or True == words.endswith("评论") or True == words.startswith("激活") or True == words.endswith("回复"):
            continue 
        if "留下你的精彩评论" in words:
            continue
        # 条件2：是中文
        if False == is_Chinese_str(words):
            continue
        # 条件3：字数
        if len(words) <= 2:
            continue
        # 条件4：右边有数字（此评估的点赞数）
        b_found_dian_zan_shu = False
        for word_result_ in json_result["words_result"]:
            if word_result_ == word_result:
                continue
            words_ = word_result_["words"]
            # 纠正一下文本
            try:
                if len(words_) < 3 and words_.endswith("B"):
                    words_ = words_.replace("B", "6")
                if words_.endswith("w"):
                    words_ = int(float(words_[:-1]) * 10000)
                location_ = word_result_["location"]
                if abs(location_["top"] - location["top"]) > 6 and location_["left"] - location["left"] > 30:
                    continue
                if False == words_.isdigit():
                    continue
                int(words_)
            except:
                continue
            # chenyj debug
            #print("哈哈，找到了此评论的点赞数")
            ping_lun_list.append({"ping_lun":words, "dian_zan_shu":int(words_)})
    return True, ping_lun_list


# In[8]:


img_path = "./评论.png"
b_has_ping_lun, ping_lun_list = get_ping_lun_ocr_result(img_path)
ping_lun_list


# In[40]:


words_ = "1.6w"
if words_.endswith("w"):
    words_ = int(float(words_[:-1]) * 10000)
print(words_)

