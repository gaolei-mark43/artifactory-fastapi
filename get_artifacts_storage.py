import requests
from multiprocessing import Pool
import time
import xlwt

url = "https://artifacts.artifactory.com/artifactory/api/search/aql"

repo_list = ['AUTO-product-public-repo', 'BDSW-product-public-repo', 'CBG-product-public-repo', 'DOXENT-product-public-repo', 'EBG-product-public-repo', 'GY-product-public-repo', 'HN-product-public-repo', 'HY-product-public-repo', 'HYKJ-product-public-repo', 'LY-product-public-repo', 'OBU-product-public-repo', 'PLBG-product-public-repo', 'RDG-product-public-repo', 'RZZL-product-public-repo', 'SE-product-public-repo', 'SEC-product-public-repo', 'STC-product-public-repo', 'TEST-product-public-repo', 'TJ-product-public-repo', 'XWH-product-public-repo', 'XXB-product-public-repo', 'YJZX-product-public-repo', 'ZHBG-product-public-repo', 'ZHYL-product-public-repo', 'ZNFW-product-public-repo', 'ZXTEST-product-public-repo']
# repo_list = ['EBG-build-repo']


docker_list = ["auto-docker-local",
"auto-docker-private",
"auto-docker-product-public",
"auto-docker-release",
"auto-docker-release-public",
"bdsw-docker-local",
"bdsw-docker-private",
"bdsw-docker-product-public",
"bdsw-docker-release",
"cbg-docker-local",
"cbg-docker-private",
"cbg-docker-product-public",
"cbg-docker-release",
"cbg-docker-release-public",
"docker-build-public",
"docker-local",
"docker-private",
"docker-selftest-repo",
"doxent-docker-local",
"doxent-docker-private",
"ebg-docker-local",
"ebg-docker-private",
"ebg-docker-product-public",
"ebg-docker-release",
"ebg-docker-release-public",
"gy-docker-local",
"gy-docker-private",
"gy-docker-product-public",
"gy-docker-release",
"gy-docker-release-public",
"hn-docker-local",
"hn-docker-private",
"hn-docker-product-public",
"hn-docker-release",
"hn-docker-release-public",
"hy-docker-local",
"hy-docker-private",
"hy-docker-product-public",
"hy-docker-release",
"hy-docker-release-public",
"ly-docker-local",
"ly-docker-private",
"ly-docker-product-public",
"ly-docker-release",
"ly-docker-release-public",
"obu-docker-local",
"obu-docker-private",
"obu-docker-product-public",
"obu-docker-release",
"obu-docker-release-public",
"plbg-docker-local",
"plbg-docker-private",
"plbg-docker-product-public",
"plbg-docker-release",
"plbg-docker-release-public",
"rdg-docker-repo",
"rzzl-docker-local",
"rzzl-docker-private",
"rzzl-docker-product-public",
"rzzl-docker-release",
"rzzl-docker-release-public",
"sec-docker-local",
"sec-docker-private",
"sec-docker-product-public",
"sec-docker-release",
"sec-docker-release-public",
"stc-docker-local",
"stc-docker-private",
"stc-docker-product-public",
"stc-docker-release",
"stc-docker-release-public",
"test-docker-local",
"test-docker-private",
"test-docker-product-public",
"test-docker-release",
"test-docker-release-public",
"tj-docker-local",
"tj-docker-private",
"xwh-docker-local",
"xwh-docker-private",
"xwh-docker-product-public",
"xwh-docker-release",
"xwh-docker-release-public",
"xxb-docker-local",
"xxb-docker-private",
"xxb-docker-product-public",
"xxb-docker-release",
"xxb-docker-release-public",
"yjzx-docker-local",
"yjzx-docker-private",
"yjzx-docker-product-public",
"yjzx-docker-release",
"yjzx-docker-release-public",
"zhbg-docker-local",
"zhbg-docker-private",
"zhbg-docker-product-public",
"zhbg-docker-release",
"zhbg-docker-release-public",
"zhyl-docker-local",
"zhyl-docker-private",
"zhyl-docker-product-public",
"zhyl-docker-release",
"zhyl-docker-release-public",
"znfw-docker-local",
"znfw-docker-private",
"znfw-docker-product-public",
"znfw-docker-release",
"znfw-docker-release-public"]

header = {
    'Content-Type': 'text/plain',
    'Authorization': 'Basic bGVpZ2FvNjpBS0NwOG5IRHIzQ2lZMnI1VmFwckZuVWVmZ01mckVGaHVZQkVDRVRkazY4Y2dWejhHTTNwWXk1YVVVNzFId1VIRTJFQmpMd29z'
}


def get_repo_size(repo):
    repo_name = repo
    payload = f'items.find({{"repo": "{repo_name}"}})\r\n'
    data23 = "items.find({\"repo\":\"STC-build-repo\",\"$and\":[{\"created\":{\"$gt\":\"2023-01-01T00:00:00.000Z\"}},{\"created\":{\"$lt\":\"2023-09-25T23:59:59.000Z\"}}]})"
    data23 = data23.replace("STC-build-repo", repo_name)
    data22 = "items.find({\"repo\":\"STC-build-repo\",\"$and\":[{\"created\":{\"$gt\":\"2022-01-01T00:00:00.000Z\"}},{\"created\":{\"$lt\":\"2022-12-31T23:59:59.000Z\"}}]})"
    data22 = data22.replace("STC-build-repo", repo_name)
    data21 = "items.find({\"repo\":\"STC-build-repo\",\"$and\":[{\"created\":{\"$gt\":\"2021-01-01T00:00:00.000Z\"}},{\"created\":{\"$lt\":\"2021-12-31T23:59:59.000Z\"}}]})"
    data21 = data21.replace("STC-build-repo", repo_name)
    data20 = "items.find({\"repo\":\"STC-build-repo\",\"$and\":[{\"created\":{\"$gt\":\"2020-01-01T00:00:00.000Z\"}},{\"created\":{\"$lt\":\"2020-12-31T23:59:59.000Z\"}}]})"
    data20 = data20.replace("STC-build-repo", repo_name)
    data19 = "items.find({\"repo\":\"STC-build-repo\",\"$and\":[{\"created\":{\"$gt\":\"2019-01-01T00:00:00.000Z\"}},{\"created\":{\"$lt\":\"2019-12-31T23:59:59.000Z\"}}]})"
    data19 = data19.replace("STC-build-repo", repo_name)

    response = requests.request("POST", url, headers=header, data=payload)
    j = 0
    for i in response.json()['results']:
        j += i['size']
    print("\n仓库："+repo_name + "\n总文件数：{}".format(response.json()['range']['total']) + "\ntotal_GB："+str(j/1024/1024/1024) + "\n")



if __name__ == '__main__':
    start_time = time.time()

    # 打印当前时间
    print("开始时间"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 换行
    pool = Pool(processes=4)  # 创建进程池，设置进程数，一般为cpu逻辑核心数
    # pool.map(get_repo_size, repo_list)  # map并发执行任务
    pool.map(get_repo_size, docker_list)  # map并发执行任务
    pool.close()  # 关闭进程池
    pool.join()  # 等子进程结束
    end_time = time.time()
    # 打印结束时间
    print("结束时间"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("耗时：{}s".format(end_time - start_time))
    # 耗时：354.1026818752289s
