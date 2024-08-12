import httpx,ujson

from action_sql import plugins_sql, qu_key


def main(l):
    id=l["qu"][9:]
    req_json=httpx.get(f"https://api.xingzhige.com/API/NetEase_CloudMusic_hotReview/?id={id}")
    req=ujson.loads(req_json.text)
    code=req["code"]
    if code==0:
        data=req["data"]
        return f"""[网易云热评] 来自：{data['artistsname']} 点赞数：{data['likedCount']}
    "{data["content"]}"
歌曲链接：{data['url']}"""
    else:
        return f'{req.get("code")} {req.get("msg")}'
if __name__=="__main__":
    plugins_sql.inf("music_wangyi_hr",0.01,"zwx08","网易云热评")
    qu_key.write("music_wy_hr","&necm_hr",1,"{plugin}.main",1)
        