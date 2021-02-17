from flask import Flask
from flask import request
import replace_element
import requests

app = Flask(__name__)

FILE_TYPE = [
    ".gif", ".png", ".jpg", ".css", ".js", ".cab",
    ".pdf", ".xsl", ".docx", ".doc", ".xslx", ".jpeg", ".csv"
]

HOST_NAME = "60.208.6.110:8080"
GOAL_NAME = "www.sdfpa119.com"

def check_file(path):
    for file in FILE_TYPE:
        if file in path:
            return True
    return False


def replace_str(old_str):
    # 替换主要信息
    old_str = old_str.replace("济南市经十路(港沟)2516号", "济南市高新区凤飞路1299号—逸家大厦-10楼东侧")
    old_str = old_str.replace("0531-85124307", "0531-88897896")
    old_str = old_str.replace("传真:85124307", "")
    old_str = old_str.replace("邮政编码:250102", "")

    # 替换不能显示的元素
    old_str = old_str.replace(replace_element.index_flash_title,
                              "<img style=\"width: 1003px; height: 189px; float: none\" src=\"https://saiyuwang-blog.oss-cn-beijing.aliyuncs.com/mypic.png\"/>")
    old_str = old_str.replace(replace_element.index_button_element, "<div/>")
    old_str = old_str.replace("EMBED", "asdasdaxz")
    old_str = old_str.replace("embed", "asdasdaxz")

    return old_str


# 把所有页面都匹配过来，加以区分
@app.errorhandler(404)
def err_handler_404(error):
    # 如果是文件类型的话，就进行301重定向
    new_url = request.url
    new_url = new_url.replace(HOST_NAME, GOAL_NAME)
    if check_file(request.url):
        return "", 301, [("location", new_url)]
    else:  # 否则就直接进行代理
        res = requests.get(new_url)
        res.encoding = "GBK"
        head_list = []
        for key in res.headers:
            head_list.append((key, res.headers.get(key)))
        n_str = res.text
        n_str = replace_str(n_str)
        return n_str


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
