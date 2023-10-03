import io
from pdfminer.high_level import extract_text
import docx2txt

async def get_docx_content(file):
    with io.BytesIO(await file.read()) as stream:
        text = docx2txt.process(stream)
    lines = text.splitlines()
    stripped_lines = [line.strip('\t').replace('\t', ' ') for line in lines]
    new_list = [x for x in stripped_lines if x.strip() != '']
    return new_list


# 获取 pdf 文件内容
async def get_pdf_content(file):
    with io.BytesIO(await file.read()) as stream:
        text = extract_text(stream)
    result = [line.strip() for line in text.split('\n') if line.strip()]
    return [text.strip() for text in result]


# 获取 txt 文件内容
async def get_txt_content(file):
    text = await file.read()
    lines = text.decode().splitlines()
    stripped_lines = [line.strip('\t').replace('\t', ' ') for line in lines]
    new_list = [x for x in stripped_lines if x.strip() != '']
    return new_list
