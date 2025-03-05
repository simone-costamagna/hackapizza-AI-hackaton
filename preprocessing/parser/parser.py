import logging
import os
import fnmatch
import re
from langchain_core.runnables import RunnablePassthrough
import fitz
import docx
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from config import OUTPUT_PREPROCESSING_MD_FILES_FOLDER
from preprocessing.config import CLASSES, HANDBOOKS
from preprocessing.parser.prompts import PROMPT_PARSE_LEGAL_CODES
from utils.wrapper import LLMWrapper

wrapper = LLMWrapper()

runnable_parse_legal_codes = ( PROMPT_PARSE_LEGAL_CODES | wrapper.llm | wrapper.parser )


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
    """
    Loads and extracts text content from various document formats in a specified folder.
    Supported formats: PDF, DOCX, HTML, TXT, and CSV.
    """
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

    logging.info(f"{len(files_content)} file loaded")

    return files_content


def classify_documents(state):
    """
    Categorizes documents based on predefined patterns in the CLASSES dictionary.
    Each document uploaded in the state is checked against class-specific patterns,
    and if matched, it is assigned to the corresponding category.
    """
    files = {class_name: [] for class_name in CLASSES}

    for file_path, content in state['files'].items():
        classified = False
        for class_name, patterns in CLASSES.items():
            for pattern in patterns:
                normalized_pattern = f"*/{pattern}" if not pattern.startswith("*/") else pattern
                if fnmatch.fnmatch(file_path, normalized_pattern):
                    files[class_name].append([file_path, content])
                    classified = True
                    break

        if not classified:
            logging.warning(f"Not classified: {file_path}")

    return files


def parse_documents(state):
    """
    Converts handbook documents into Markdown format.
    Checks if a preprocessed Markdown file exists; if so, it reads the content.
    Otherwise, it processes the document using 'runnable_parse_legal_codes'
    """
    for file in tqdm(state['files'][HANDBOOKS], desc="Converting to md format"):
        file_name = os.path.basename(file[0])
        md_file_path = os.path.join(OUTPUT_PREPROCESSING_MD_FILES_FOLDER, os.path.splitext(file_name)[0] + '.md')

        if os.path.exists(md_file_path):
            with open(md_file_path, 'r', encoding='utf-8') as md_file:
                content = md_file.read()
        else:
            content = runnable_parse_legal_codes.invoke({'content': file[1]})
            content = re.sub(r'markdown\.\.\.\`{3}', '', content, flags=re.IGNORECASE)

            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(content)

        file[1] = content

    logging.info(f"{len(state['files'][HANDBOOKS])} files parsed to md")

    return state['files']


parser = (
    RunnablePassthrough.assign(files=load_documents)
    | RunnablePassthrough.assign(files=classify_documents)
    | RunnablePassthrough.assign(files=parse_documents)
)