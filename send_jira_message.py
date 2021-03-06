import requests
import json
from jira import JIRA
import time,datetime

#登录jira
def search_jira():
    time = datetime.datetime.now().strftime('%Y - %m - %d')
    print(time)
    # AND created >= 2020 - 03 - 06
    # AND created <= 2020 - 03 - 07
    jira = JIRA('https://jira.daocloud.io', basic_auth=('jing.yu', 'YUJINGguanguo99%'))
    issue_new = len(jira.search_issues('project = SOL AND resolution = Unresolved AND labels = 移动展业 ORDER BY labels ASC, priority DESC, updated DESC',maxResults=1000))
    issue_fixed = len(jira.search_issues('project = "DX" AND Sprint = "538" AND status = "Fixed"',maxResults=1000))
    issue_verified = len(jira.search_issues('project = "DX" AND Sprint = "538" AND status = "verified"', maxResults=1000))
    return {"new_num":issue_new,"fixed_num":issue_fixed,"verified_num":issue_verified}

#企业微信发送数据
def send_message():
    num = search_jira()
    new_num = num.get("new_num")
    fixed_num = num.get("fixed_num")
    verified_num = num.get("verified_num")
    print(new_num, fixed_num, verified_num)


    post_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ed02f420-63dd-4a45-8816-28c979795d5f'

    header = {
        "Content-Type": "application/json"
    }
    #markdown格式数据
    payload = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "content": f"DX DMP 2.3.0\n>* <font color=\"warning\">待修复：{new_num}</font>\n>* <font color=\"comment\">已修复：{fixed_num}</font>\n >* <font color=\"info\">已验证：{verified_num}</font>\n  "
                       ">* [JIRA链接](https://jira.daocloud.io/secure/RapidBoard.jspa?rapidView=305&projectKey=DX&view=detail&selectedIssue=DX-955&sprint=567)"
        }
    })
    payload = payload.encode("utf-8")
    response = requests.request("POST", post_url , data = payload)


#设置定时发送的时间
# def send_time():
#     while 1 == 1:
#         dt_ms = datetime.datetime.now().strftime('%H:%M:%S')
#         if dt_ms == "09:50:00" or dt_ms == "17:50:00":
#             send_message()
#             time.sleep(60)
#             continue

search_jira()