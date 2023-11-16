# 简历信息提取系统

[TOC]

## 介绍

你是否曾在庞杂的简历堆中迷失？你是否对于手动输入无休止的文本信息而感到无奈？那么，是时候让简历信息提取系统为你解忧了。这个系统，不仅仅是一个技术产物，更是一位贴心的助手，它可以从图片中提炼出文字，将一幅幅静态的简历转化为动态的、可编辑的文本。用户只需轻松上传图片，简历信息提取系统即刻展开它的魔法，精准地捕捉图中文字，甚至连字体、大小都能一一辨识。而在信息提取之后，它还能将这些文字整理成有序的格式，让用户可以方便地编辑和管理。这不仅是一次技术的革新，更是一次用户体验的飞跃。简历信息提取系统以其独特的方式，将人与信息、图像与文字紧密相连，让我们在处理简历的道路上，不再孤单，不再困扰。它就像是桌面上的一位小精灵，时刻为我们解决问题，为我们的工作带来便利与乐趣。

## 主要功能

1. **简历上传**：用户可以上传word文档格式的简历。
2. **信息提取**：系统能够自动识别并提取word文档中的文字信息。
3. **结构化输出**：提取出的信息将以结构化的文字格式呈现。
4. **人岗匹配**：将简历信息与已有的岗位信息进行匹配，为每个求职者找到最适合的岗位。

## 组织结构

本项目采用模块化的组织结构，主要分为以下几个模块：

- **用户界面(UI)**：负责与用户的交互，包括文件上传、信息展示和编辑等功能。
- **文字识别**：利用大模型对word文档进行文字信息的提取。
- **信息处理**：对提取出的文字信息进行进一步处理，实现结构化输出。
- **数据存储**：负责系统中数据的存储和管理。
- **人岗匹配**：根据结构化的简历和岗位信息，为求职者匹配岗位。


## 目录说明

```
├─Assets	相关图片
├─Express	后端，用于word转txt
├─FastApi	 后端，用于封装模型
├─Frontend	前端
├─SpringBoot	后端，用于用户管理
├─Sql	数据库建表
├─Train	模型训练
│  └─classfication	分类器
│  └─ner	命名实体识别
│  └─test	模型测试
├─Utils	工具
│  └─format	格式转换
│  └─gather	分类数据采集
```

## 小组成员分工

| 姓名   | 分工           | 负责模块       | 职责描述                                         |
|------|--------------|--------------|------------------------------------------------|
| 秦声鸿  | 项目经理       | 整体协调       | 负责项目的整体协调和管理，解决项目中出现的问题；帮助进行AI模型的训练和修改一些bug       |
| 童维希  | 前端开发工程师   | 用户界面(UI)    | 负责用户界面的设计和开发，实现用户与系统的交互       |
| 胡宇飞  | AI工程师   | word文档处理、信息提取、人岗匹配 | 负责word文档处理、信息提取、人岗匹配模块和人岗匹配模块的开发，提高识别的准确率   |
| 罗琳程  | 后端开发工程师      | 后端       | 负责系统中后端模块的开发，包括数据库和业务逻辑    |

## 项目运行

### 前端

```shell
npm install

npm run serve-dev
```

### 后端

#### FastAPI

1. 下载模型到`FastApi/models`目录下

   链接：https://pan.baidu.com/s/1pRfDXOTXKtjZ5AFQJmH81w?pwd=883h ，提取码：883h

2. 在`FastApi`目录下建立`secrets.txt`

   ```txt
   [key]
   jwt_key=XXX
   ```

   其中 XXX 为自定义的`jwt`密钥

#### Spring Boot

1. `SpringbootApplication.java`中是通过`@PropertySource("classpath:secrets.txt")`注解进行相关数据的读取，在`Springboot/src/main/resources`下建立`secrets.txt`并根据目录中的 yaml 配置文件填入键值对
   
2. cd 到 `Springboot` 目录，运行命令`./mvnw spring-boot:run`

#### Express

`Express`中使用了`mammoth`来解析`docx`文件，可以作为`docx2txt`的替代品使用。在某些情况下`mammoth`的解析结果更加准确，具体体现在实际测试中`docx2txt`会重复读取两次内容

你可以在`FastApi/document.py`中自行选择其一作为解析工具

```py
# import httpx
import docx2txt

# 方法A 向Express发送请求，通过js库mammoth获取内容
# async def get_docx_content(file):
#     # url = 'http://127.0.0.1:3010/analysis-docx-file/'
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, files={"file": file.file})
#         if response.status_code != 400:
#             return eval(response.text)
#         else:
#             raise Exception

# 方法B 通过python库docx2txt获取内容
async def get_docx_content(file):
    with io.BytesIO(await file.read()) as stream:
        text = docx2txt.process(stream)
    lines = text.splitlines()
    stripped_lines = [line.strip('\t').replace('\t', ' ') for line in lines]
    new_list = [x for x in stripped_lines if x.strip() != '']
    return new_list
```

如果使用`Express`需要在该模块下执行

```shell
node app.js