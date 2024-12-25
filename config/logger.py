import os
import logging
from config.env import FASTAPI_ROOT_PATH


def setup_logger(log_file_path):
    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # 使用更灵活的配置方式而不是 basicConfig
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    # 文件处理器
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # 控制台处理器
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(file_handler)
    # logger.addHandler(stream_handler)

    return logger


# 设置日志文件路径
log_file_path = f'{FASTAPI_ROOT_PATH}/log/logger/logger.log'
logger = setup_logger(log_file_path)
