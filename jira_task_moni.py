import requests
import json
from jira import JIRA
import time,datetime

#登录jira，并获取jira数据
def search_jira():
    # time = datetime.datetime.now().strftime('%Y - %m - %d')
    # AND created >= 2020 - 03 - 06
    # AND created <= 2020 - 03 - 07
    jira = JIRA('https://jira.daocloud.io', basic_auth=('jing.yu', 'YUJINGguanguo99%'))
    delay_num_moni = len(jira.search_issues('project = SOL AND resolution = Unresolved AND due < "0"',maxResults=1000))
    daoqi_num_moni = len(jira.search_issues('project = SOL AND resolution = Unresolved AND due = 0d',maxResults=1000))
    done_num_night = len(jira.search_issues('project = SOL AND resolution in (Done, 完成) AND updated >= -1d',maxResults=1000))
    update_num_night = len(jira.search_issues('project = SOL AND resolution = Unresolved AND updated >= -1d',maxResults=1000))

    return {"delay_num_moni": delay_num_moni,
            "daoqi_num_moni": daoqi_num_moni,
            "done_num_night": done_num_night,
            "update_num_night": update_num_night
            }


#企业微信发送数据
def send_moni_message():
    num = search_jira()
    delay_num_moni = num["delay_num_moni"]
    daoqi_num_moni = num["daoqi_num_moni"]
    post_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=074e0adc-40a5-478a-a7f3-5fbc38c6bc2b'
    header = {
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "content": f"### 今日待处理任务\n >* 到期：[{daoqi_num_moni}](https://jira.daocloud.io/issues/?filter=13485)\n >* <font color=\"warning\">已逾期</font>：[{delay_num_moni}](https://jira.daocloud.io/issues/?filter=13483)"
        }
    })

    payload = payload.encode("utf-8")
    response = requests.request("POST", post_url , data = payload)

def send_night_message():
    num = search_jira()
    done_num_night = num["done_num_night"]
    update_num_night = num["update_num_night"]
    print(done_num_night,done_num_night)


    post_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=074e0adc-40a5-478a-a7f3-5fbc38c6bc2b'

    header = {
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "content": f"### 今日任务完成状态\n >* <font color=\"info\">已完成</font>：[{done_num_night}](https://jira.daocloud.io/issues/?filter=13486)\n>* 已更新：[{update_num_night}](https://jira.daocloud.io/issues/?filter=13487)"
        }
    })

    payload = payload.encode("utf-8")
    response = requests.request("POST", post_url , data = payload)

# send_night_message()
#执行早上九点半发送消息
send_moni_message()