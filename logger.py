import logging
import os
from datetime import datetime

base_application_path = os.getcwd()
log_folder_name = 'logs'

log_path = os.path.join(base_application_path, log_folder_name)

try:
    os.makedirs(log_path, exist_ok=True)
    
    log_file = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
    log_file_path = os.path.join(log_path, log_file)

    logging.basicConfig(
        level=logging.INFO,  
        filename=log_file_path, 
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s" 
    )
    
    logging.info(f"Logger configured successfully to: {log_file_path}")

except OSError as e:
    print(f"ERROR (logger.py): Could not create log directory or file at {log_path}. Error: {e}")
    print("Falling back to console logging.")
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
    logging.error("Failed to set up file logging. Logging to console instead.")
except Exception as e:
    print(f"ERROR (logger.py): An unexpected error occurred during logging setup: {e}")
    print("Falling back to console logging.")
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
    logging.error("Failed to set up file logging. Logging to console instead due to unexpected error.")