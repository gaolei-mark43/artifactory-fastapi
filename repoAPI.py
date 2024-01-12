
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import datetime
import os
import ast
import enum



app = FastAPI()
aql_url = "https://depend.artifactory.com/artifactory/api/search/aql"
base_url = "https://depend.artifactory.com/artifactory/api/"
headers = {
    'Authorization': 'Basic bGVpZ2FvNjpBS0NwOG5HanJoNVd6ZUxxXXXXXXXXX3JpSXXXXXXXXXXXXXXXXXXXXXXXFxdnM0cG1uXXXXXXXX28xZ2NrcHBGSGJW'
}

aliyun_headers = {
    'Authorization': 'Basic bGVpZ2FvNjpBS0NwOG5HanJoNVd6ZUxxXXXXXXXXX3JpSXXXXXXXXXXXXXXXXXXXXXXXFxdnM0cG1uXXXXXXXX28xZ2NrcHBGSGJW=='
}

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def display():
    return "Hello Artifactory!"


# 获取存储总表
@app.get("/storageinfo")
def get_self_storage_data():
    url = base_url + "storageinfo/"
    response = requests.get(url, headers=headers)
    storage_data = response.json()
    return storage_data['repositoriesSummaryList']


# 获取单表存储
@app.get("/storageinfo/{repo_name}")
def get_self_storage_data(repo_name):
    url = base_url + "storageinfo/"
    response = requests.get(url, headers=headers)
    storage_data = response.json()
    for i in storage_data['repositoriesSummaryList']:
        if i['repoKey'] == repo_name:
            return i


# 获取虚拟库
@app.get("/virtual_repo")
def get_repo_data():
    url = base_url + "repositories?type=virtual"
    response = requests.get(url, headers=headers)
    repo_data = response.json()
    return repo_data


# 获取远程库
@app.get("/remote_repo")
def get_repo_data():
    url = base_url + "repositories?type=remote"
    response = requests.get(url, headers=headers)
    repo_data = response.json()
    return repo_data


# 获取本地库
@app.get("/local_repo")
def get_repo_data():
    url = base_url + "repositories?type=local"
    response = requests.get(url, headers=headers)
    repo_data = response.json()
    return repo_data


# 获取单库数据
@app.get("/repo/{repo_name}")
def get_self_repo_data(repo_name: str):
    url = base_url + "repositories/" + repo_name
    response = requests.get(url, headers=headers)
    repo_data = response.json()
    return repo_data


# aliyun虚拟库
@app.get("/aliyun_virtual_repo")
def get_self_repo_data():
    url = "http://10.10.100.101:8081/artifactory/api/repositories/?type=remote"
    response = requests.get(url, headers=aliyun_headers)
    repo_data = response.json()
    return repo_data


# 私服锁定用户
@app.get("/depnd_lock_user")
def get_depnd_lock_user():
    url = base_url + "security/lockedUsers"
    response = requests.get(url, headers=headers)
    lock_user = response.json()
    return lock_user


# 公网制品锁定用户
@app.get("/pub_artifacts_lock_user")
def get_pub_artifacts_lock_user():
    url = "https://artifacts-pub.artifactory.com/artifactory/api/security/lockedUsers"
    token = {
        'Authorization': 'Basic bGVpZ2FvNjpBS0NwOGs4RVMyd2NGaFBqdUdGNWNCMjl1WUJOUEVnTUFpWEV3cFlUcmVIQzhjRjRROXlLMThwazF0b1BVVUZ1aW0ydVVQc3lW'
    }
    response = requests.get(url, headers=token)
    lock_user = response.json()
    return lock_user


# 办公网制品锁定用户
@app.get("/artifacts_lock_user")
def get_artifacts_lock_user():
    url = "https://artifacts.artifactory.com/artifactory/api/security/lockedUsers"
    token = {
        'Authorization': 'Basic bGVpZ2FvNjpBS0NwOG5IRHIzQ2lZMnI1VmFwckZuVWVmZ01mckVGaHVZQkVDRVRkazY4Y2dWejhHTTNwWXk1YVVVNzFId1VIRTJFQmpMd29z'
    }
    response = requests.get(url, headers=token)
    lock_user = response.json()
    return lock_user


# 解锁ARF用户
@app.get("/unlock_all_user")
def unlock_all_user():
    start_time = time.time()
    artifacts_url = "https://artifacts.artifactory.com/artifactory/api/security/unlockUsers"
    pub_artifacts_url = "https://artifacts-pub.artifactory.com/artifactory/api/security/unlockUsers"
    artifacts_token = {
        'Authorization': 'Basic bGVpZ2FvNjpBS0NwOG5IRHIzQ2lZMnI1VmFwckZuVWVmZ01mckVGaHVZQkVDRVRkazY4Y2dWejhHTTNwWXk1YVVVNzFId1VIRTJFQmpMd29z'
    }
    pub_artifacts_token = {
        'Authorization': 'Basic bGVpZ2FvNjpBS0NwOGs4RVMyd2NGaFBqdUdGNWNCMjl1WUJOUEVnTUFpWEV3cFlUcmVIQzhjRjRROXlLMThwazF0b1BVVUZ1aW0ydVVQc3lW'
    }
    lock_user = get_artifacts_lock_user()
    print(lock_user)
    pub_lock_user = get_pub_artifacts_lock_user()
    for i in lock_user:
        response = requests.post(artifacts_url+"/{}".format(i), headers=artifacts_token, data=i)
        print(response.text)

    for i in pub_lock_user:
        requests.post(pub_artifacts_url+"/{}".format(i), headers=pub_artifacts_token, data=i)
    end_time = time.time()
    return {"msg": "解锁耗时:{}".format(end_time-start_time)}


# 查询单库下载数据
def get_search_data(repo_name):
    repo_name = repo_name
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    payload = f"items.find({{\r\n    \"repo\":{{\"$eq\":\"{repo_name}\"}},\r\n    \"$and\":[{{\"stat.downloaded\":{{\"$gt\" : \"{today}T00:00:00.00+08:00\"}}}}]\r\n    }}).include(\"name\", \"repo\", \"path\", \"stat.downloaded\",\"stat.downloads\",\"stat.downloaded_by\")\r\n"
    headers = {
            'Content-Type': 'text/plain',
            'Authorization': 'Basic bGVpZ2FvNjpBS0NwOG5HanJoNVd6ZUxxXXXXXXXXX3JpSXXXXXXXXXXXXXXXXXXXXXXXFxdnM0cG1uXXXXXXXX28xZ2NrcHBGSGJW'
        }
    response = requests.request("POST", aql_url, headers=headers, data=payload)
    download_data = []
    for item in response.json()['results']:
        download_data.append(item)
    tuple_data = ()
    if len(download_data) == 0:
        repo = repo_name
        data = None
        return data, repo
    else:
        for i in download_data:
            data = (i['name'], i['stats'][0]['downloaded'], i['repo'], i['path'], i['stats'][0]['downloaded_by'], i['stats'][0]['downloads'])
            tuple_data += (data,)
            repo = i['repo']
        return tuple_data, repo


# 默认展示下载数据
@app.get('/table/')
def display_table():
    repo_name = 'stc-mvn-release-private'
    data, _ = get_search_data(repo_name)
    return data, repo_name


# 查询单库下载数据
@app.get('/table/{repo_name}')
def query_table(repo_name):
    data, _ = get_search_data(repo_name)
    return data, repo_name


# npm枚举
class NpmRepoName(enum.Enum):
    npm_repo_name1 = "npm-repo"
    npm_repo_name2 = "ebg-npm-private"
    npm_repo_name3 = "npm-private"
    npm_repo_name4 = "zhyl-npm-private"
    npm_repo_name5 = "npm-private-npm.flyui.cn"
    npm_repo_name6 = "npm-remote-npmmirror-cache"
    npm_repo_name7 = "npm-remote-npmmirror-new-cache"


# maven-private枚举
class Maven_Local_Name(enum.Enum):
    mvn_local_name0 = "mvn-3rd-private"
    mvn_local_name = "auto-mvn-release-private"
    mvn_local_name1 = "auto-mvn-snapshot-private"
    mvn_local_name2 = "bdsw-mvn-release-private"
    mvn_local_name3 = "bdsw-mvn-snapshot-private"
    mvn_local_name4 = "cbg-mvn-release-private"
    mvn_local_name5 = "cbg-mvn-snapshot-private"
    mvn_local_name6 = "ebg-mvn-release-private"
    mvn_local_name7 = "ebg-mvn-snapshot-private"
    mvn_local_name8 = "gy-mvn-release-private"
    mvn_local_name9 = "gy-mvn-snapshot-private"
    mvn_local_name10 = "hy-mvn-release-private"
    mvn_local_name11 = "hy-mvn-snapshot-private"
    mvn_local_name12 = "ly-mvn-release-private"
    mvn_local_name13 = "ly-mvn-snapshot-private"
    mvn_local_name14 = "obu-mvn-release-private"
    mvn_local_name15 = "obu-mvn-snapshot-private"
    mvn_local_name16 = "plbg-mvn-release-private"
    mvn_local_name17 = "plbg-mvn-snapshot-private"
    mvn_local_name18 = "sec-mvn-release-private"
    mvn_local_name19 = "sec-mvn-snapshot-private"
    mvn_local_name20 = "stc-mvn-release-private"
    mvn_local_name21 = "stc-mvn-snapshot-private"
    mvn_local_name22 = "xxb-mvn-release-private"
    mvn_local_name23 = "xxb-mvn-snapshot-private"
    mvn_local_name24 = "zhbg-mvn-release-private"
    mvn_local_name25 = "zhbg-mvn-snapshot-private"
    mvn_local_name26 = "zhyl-mvn-release-private"
    mvn_local_name27 = "zhyl-mvn-snapshot-private"
    mvn_local_name28 = "znfw-mvn-release-private"
    mvn_local_name29 = "znfw-mvn-snapshot-private"
    mvn_local_name30 = "auto-mvn-3rd-private"
    mvn_local_name31 = "bdsw-mvn-3rd-private"
    mvn_local_name32 = "cbg-mvn-3rd-private"
    mvn_local_name33 = "ebg-mvn-3rd-private"
    mvn_local_name34 = "gy-mvn-3rd-private"
    mvn_local_name35 = "hy-mvn-3rd-private"
    mvn_local_name36 = "ly-mvn-3rd-private"
    mvn_local_name37 = "obu-mvn-3rd-private"
    mvn_local_name39 = "sec-mvn-3rd-private"
    mvn_local_name40 = "stc-mvn-3rd-private"
    mvn_local_name41 = "xxb-mvn-3rd-private"
    mvn_local_name42 = "zhbg-mvn-3rd-private"
    mvn_local_name43 = "zhyl-mvn-3rd-private"
    mvn_local_name44 = "znfw-mvn-3rd-private"


# maven-remote
@app.get('/mvn_remote')
def remote():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    # 增加一个正则匹配，匹配值以-cache结尾以mvn开头
                    if line[0].endswith("-cache") and line[0].startswith("mvn"):
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# maven-local
@app.get('/mvn_local')
def mvn_local():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if line[0] in [item.value for item in Maven_Local_Name]:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# npm
@app.get('/npm')
def npm():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if line[0] in [item.value for item in NpmRepoName]:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# pypi
@app.get('/pypi')
def pypi():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if "pypi" in line[0]:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# cocoapods
@app.get('/cocoapods')
def cocoapods():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    # 校验库名称
                    if line[0] == "cocoapods-luck-private":
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# conan
@app.get('/conan')
def conan():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if "conan" in line[0] and "conan-remote-bintray.com-cache" not in line[0] and "conan-remote-conan.bintray.com-cache" not in line[0]:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# conda
@app.get('/conda')
def conda():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if "conda" in line[0]:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# pub
@app.get('/pub')
def conda():
    data = []
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if "pub-" in line[0]:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data


# temp
@app.get('/mvn_temp')
def mvn_temp():
    data = []
    # 排除列表
    exclude_list = [
        "mvn-temp-3rdParty-allowRedeploy",
        "mvn-temp-CIT-3rdParty",
        "mvn-temp-CheZaiDaoHang-snapshot",
        "mvn-temp-MS-snapshot",
        "mvn-temp-RS-3rdParty",
        "mvn-temp-RS-odeon-3rdParty",
        "mvn-temp-TC-3rdParty",
        "mvn-temp-TESTyzma-3rdParty",
        "mvn-temp-YGNOME-3rdParty",
        "mvn-temp-YGNOME-release",
        "mvn-temp-YGNOME-snapshot",
        "mvn-temp-ZF-3rdParty",
        "mvn-temp-release-CheZaiDaoHang"
    ]
    for filename in os.listdir("/home/gaolei/schedule_task/get_depend_daily_download_count"):
        if filename.endswith(".txt"):
            filepath = os.path.join("/home/gaolei/schedule_task/get_depend_daily_download_count", filename)
            with open(filepath) as f:
                content = f.read()
                lines = ast.literal_eval(content)
                for line in lines:
                    if "mvn-temp" in line[0] and line[0] not in exclude_list:
                        name, downloads, date_str = line[0], line[1], line[2]
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        data.append((name, downloads, date))
    data.sort(key=lambda x: x[2])
    groups = {}
    for name, downloads, date in data:
        if name not in groups:
            groups[name] = {"x": [], "y": []}
        groups[name]["x"].append(date)
        groups[name]["y"].append(downloads)
    chart_data = []
    for name, values in groups.items():
        chart_data.append({"name": name, "data": list(zip(values["x"], values["y"]))})
    return chart_data



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='172.31.65.60', port=9098)


