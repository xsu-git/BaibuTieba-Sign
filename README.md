
[![](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://www.python.org/downloads/)

- 该项目会长期更新。
- 欢迎提issue，维护者看到后都会积极回答。

## 百度贴吧每日自动签到 :octocat:

本项目使用`Github Action`来部署自动签到程序，无需自己购买服务器，安全可靠且方便。另外支持钉钉机器人通知。

### 使用方式

1. `fork`本项目。

![Fork项目](https://tva1.sinaimg.cn/large/008i3skNgy1gvbcpgto6dj620k0u079i02.jpg)

2. 依次点击【Setting】、【Secrets】、【New repository secret】。

![New repository secret](https://tva1.sinaimg.cn/large/008i3skNgy1gvbct5z1laj61yc0u0jwe02.jpg)

3. 把 Name 设置为`COOKIE`这个字符串，Value 设置为`自己贴吧账号的Cookie`。

![action-secrets](https://tva1.sinaimg.cn/large/008i3skNgy1gvbcyg7krpj61wl0u0whm02.jpg)

4. 百度贴吧的 Cookie 可以在贴吧首页F12打开开发者工具，然后依次点击【Network】、【Fetch/XHR】（或者【XHR】）、【任一 Name】查看是否有`cookie`字段，如果没有可以换一个接口试试，找到后复制`cookie`的值，粘贴到上面 Value 处，并点击【Add secret】。

![get_cookie](https://tva1.sinaimg.cn/large/008i3skNgy1gvbd63xbr1j61ve0u0tk902.jpg)

5. 允许 Github Actions 工作流。

![enable](https://tva1.sinaimg.cn/large/008i3skNgy1gvbd0y864mj61k60ry41502.jpg)

### 签到时间修改

本程序默认是在北京时间凌晨 2 点去执行，如果需要修改签到时间，可以修改`.github/workflows/check_in.yml`文件中的`cron`字段，该字段文档可以[查看这里](https://docs.github.com/en/actions/reference/events-that-trigger-workflows)。

### 接入钉钉机器人

签到结果可以在`贴吧`和`Github Action`上查看，如果需要更加实时的查看信息，这个时候考虑接入钉钉机器人，具体如下：

1. 创建一个打卡群。点击钉钉右上角的加号，再点击【发起群聊】，选择一个非公司的群，如【考试群】。

![建群](https://tva1.sinaimg.cn/large/008i3skNgy1gvbdb03u9vj611m0u0dhi02.jpg)

2. 输入喜欢的群名称，然后点击【创建】。

3. 在群内点击右上角设置按钮，然后依次点【智能群助手】、【添加机器人】、【自定义】、【添加】。

![添加机器人](https://tva1.sinaimg.cn/large/008i3skNgy1gvbdba2gdxj611u0tu0vs02.jpg)

4. 给机器人起一个名字，然后点【加签】，并复制秘钥的内容（秘钥有点长，要复制输入框内的所有内容）。

![加签](https://tva1.sinaimg.cn/large/008i3skNgy1gvbdcxzaflj61160tq76c02.jpg)

5. 在 Github 的 Secrets 中在添加一个变量，Name 是`DINGTALK_SECRET`，Value 是刚才复制的内容（操作过程可以参考上面【使用方式】第 2、3 步）。

![添加DINGTALK_SECRET](https://tva1.sinaimg.cn/large/008i3skNgy1gvbdj79mvpj61ye0u0q6802.jpg)

6. 完成后复制`Webhook`的内容。

![复制Webhook](https://tva1.sinaimg.cn/large/008i3skNgy1gvbdcxzaflj61160tq76c02.jpg)

7. 在 Github 的 Secrets 中在添加一个变量，Name 是`DINGTALK_WEBHOOK`，Value 是刚才复制的内容。

![添加DINGTALK_WEBHOOK](https://tva1.sinaimg.cn/large/008i3skNgy1gvbdn4tz9dj61xi0u0q6902.jpg)

8. 返回钉钉完成即可，由于我们是凌晨签到的，如果害怕大半夜推送打扰到自己，可以把群设置成消息免打扰。

## 重要声明 :loudspeaker:
该项目开发的初衷是为了学术研究。


