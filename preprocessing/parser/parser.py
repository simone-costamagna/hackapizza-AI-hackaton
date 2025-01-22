import logging
import os
from langchain_core.runnables import RunnablePassthrough
import fitz
import docx
from bs4 import BeautifulSoup
import csv
from preprocessing.config import CLASSES, LEGAL_CODES
from preprocessing.parser.prompts import PROMPT_PARSE_LEGAL_CODES
from utils.wrapper import LLMWrapper


wrapper = LLMWrapper()


def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        text += page.get_text()
    return text


def load_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    text = "\n".join(full_text).strip()

    return text


def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    text = soup.get_text(separator="\n").strip()
    return text


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        return text


def load_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        csv_content = []
        for row in reader:
            csv_content.append(", ".join(row))
        text = "\n".join(csv_content).strip()
        return text


def load_documents(state):
    folder_path = state['data_folder_path']

    files_content = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            text = None
            file_path = os.path.join(root, file)

            if not 'domande' in file_path:
                if file.lower().endswith('.pdf'):
                    text = load_pdf(file_path)
                elif file.lower().endswith('.docx'):
                    if not 'Codice Galattico' in file_path: # Do not repeat the reading
                        text = load_docx(file_path)
                elif file.lower().endswith('.html'):
                    text = load_html(file_path)
                elif file.lower().endswith('.txt'):
                    text = load_txt(file_path)
                elif file.lower().endswith('.csv'):
                    text = load_csv(file_path)
                else:
                    logging.warning(f"No parser for: {file_path}")

                if text:
                    files_content[file_path] = text

    logging.info(f"{len(files_content)} file proccessed")

    return files_content


def classify_documents(state):
    files = {class_name: [] for class_name in CLASSES}

    for file_path, content in state['files'].items():
        classified = False

        for class_name, keywords in CLASSES.items():
            if any(keyword in file_path for keyword in keywords):
                files[class_name].append([file_path, content])
                classified = True
                break

        if not classified:
            logging.warning(f"Not classified: {file_path}")

    return files


def parse_documents(state):
    for file in state['files'][LEGAL_CODES]:
        content = ({ 'content': file[1]} | PROMPT_PARSE_LEGAL_CODES | wrapper.llm)
        file[1] = content

    return state['files']


parser = (
    RunnablePassthrough.assign(files=load_documents)
    | RunnablePassthrough.assign(files=classify_documents)
    | RunnablePassthrough.assign(files=parse_documents)
)