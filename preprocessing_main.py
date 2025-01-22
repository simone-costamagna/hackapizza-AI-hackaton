from config import DATA_FOLDER_PATH
from preprocessing.parser.parser import parser
from log_config.log_config import setup_logging

setup_logging()

input = {
    'data_folder_path': DATA_FOLDER_PATH,
}

chain = (
    parser
)

res = chain.invoke(input)


