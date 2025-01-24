import logging
import os
from langchain_core.runnables import RunnablePassthrough
import fitz
import docx
from bs4 import BeautifulSoup
import csv
from config import DATA_FOLDER_PATH
from knowledge_base.config import CLASSES, GRAPH_DB, VECTOR_DB, TEMPLATE
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
        matrix = [row for row in reader]
    return matrix


def load_md(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to load .md file: {file_path} | Error: {e}")
        return None


def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json_file.read()
    except Exception as e:
        logging.error(f"Failed to load JSON file: {file_path} | Error: {e}")
        return None


def load_file(file_name, file_path):
    try:
        if 'domande' in file_path:  # Skip 'domande' files
            return None

        if file_name.lower().endswith('.pdf'):
            return load_pdf(file_path)
        elif file_name.lower().endswith('.docx'):
            if 'Codice Galattico' not in file_path:  # Avoid duplicate reads
                return load_docx(file_path)
        elif file_name.lower().endswith('.html'):
            return load_html(file_path)
        elif file_name.lower().endswith('.txt'):
            return load_txt(file_path)
        elif file_name.lower().endswith('.csv'):
            return load_csv(file_path)
        elif file_name.lower().endswith('.md'):
            return load_md(file_path)
        elif file_name.lower().endswith('.json'):
            return load_json(file_path)
        else:
            logging.warning(f"No parser for: {file_path}")
            return None
    except Exception as e:
        logging.error(f"Error loading file: {file_path} | {e}")
        return None


def load_documents(state):
    files = {
        GRAPH_DB: [],
        VECTOR_DB: [],
        TEMPLATE: []
    }

    logging.info(f"Started loading {DATA_FOLDER_PATH} documents")
    for db_type, paths in CLASSES.items():
        for path in paths:
            if os.path.isfile(path):  # If the path is a file
                file_name = os.path.basename(path)
                text = load_file(file_name, path)
                if text:
                    files[db_type].append([path, text])
            elif os.path.isdir(path):  # If the path is a folder
                for root, _, file_names in os.walk(path):
                    for file in file_names:
                        file_path = os.path.join(root, file)
                        text = load_file(file, file_path)
                        if text:
                            files[db_type].append([file_path, text])

    logging.info(f"Files loaded")

    return files


loader = (
    RunnablePassthrough.assign(files=load_documents)
)