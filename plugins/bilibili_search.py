import httpx,ujson
import yaml
from action_sql import plugins_sql, qu_key
from more_action import send_art, send_msg


def main(l):
    msg=l["qu"][10:]
    msg=msg.strip()
    #msg=msg.replace(" ","+")
    print(msg)
    wxid=l["wxid"]
    req_json=httpx.get(f'https://api.xingzhige.com/API/b_search/?msg={msg}&n=1')
    #req_json=httpx.post('https://api.xingzhige.com/API/b_search/',data={"msg":msg,"n":1})
    print(req_json.content)
    req=ujson.loads(req_json.content)
    #print(req)
    if "code" not in req:
        data=req[0]
        if data==None:
            return "无搜索结果"
        linktype=data.get("linktype")
        if linktype=="video":
            msg_=f"""{data['title']}
    up:{data['up']}
    mid:{data['mid']}
    see:{data['see']}
    time:{data['time']}
    time_video:{data['time_video']}
    aid:{data['aid']}
    bvid:{data['bvid']}"""
            send_msg(wxid,msg_)
            send_art(data['up'],wxid,data['cover'],data['title'],f"https://www.bilibili.com/video/{data['bvid']}")
        elif linktype=="app_user":
            msg_=f"""{data['name']}
    mid:{data['mid']}
    level:{data['level']}
    fans:{data['fans']}
    desc:{data['desc']}"""
            send_msg(wxid,msg_)
            send_art(data['desc'],wxid,data['cover'],data['name'],f"https://space.bilibili.com/{data['mid']}")
        elif linktype=="bgm_media":
            msg_=f"""{data['title']}
    season_id:{data['season_id']}
    season_type_name:{data['season_type_name']}
    style:{data['style']}
    styles:{data['styles']}
    cv:{data['cv']}
    staff:{data['staff']}"""
            send_msg(wxid,msg_)
            send_art(f"""{data['season_type_name']}
{data['style']}
{data['styles']}
{data['cv']}
{data['staff']}""",wxid,data['cover'],data['title'],f"https://www.bilibili.com/bangumi/play/ss{data['season_id']}")
        elif linktype=="live":
            msg_=f"""{data['title']}
    user_name:{data['name']}
    roomid:{data['roomid']}
    mid:{data['mid']}"""
            send_msg(wxid,msg_)
            send_art(data['name'],wxid,data['cover'],data['title'],f"https://live.bilibili.com/{data['roomid']}")

        else:
            msg_=yaml.dump(data, sort_keys=False, default_flow_style=False,allow_unicode=True)
            send_msg(wxid,msg_)
    #elif req["code"]==-400:
    #    return "请求错误(-400)"
    #elif req["code"]==-401:
    #    return "参数丢失(-401)"
    else:
        return f'{req.get("code")} {req.get("message")}'
    
if __name__=="__main__":
    plugins_sql.inf("bilibili_search",0.01,"zwx08","b站搜索")
    qu_key.write("b_search","&b_search",1,"{plugin}.main",1)
