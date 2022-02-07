import re
import time
from pathlib import PosixPath
import shutil
from collections import Counter
from concurrent.futures import as_completed, ProcessPoolExecutor

import multiprocessing
from pathlib import PosixPath
import shutil
import typing

from tqdm import tqdm

from hrflow_importer.utils.file_handler import FileHandler
from hrflow_importer.utils.config.config import config #TODO better import from init

# TODO cli args or Env Variables
LOCAL_FILES_FOLDER = config.LOCAL_FILES_FOLDER#"files"
LOCAL_FAILURES_FOLDER = config.LOCAL_FAILURES_FOLDER#"failures"


def send_file_to_hrflow(client, source_key, filename, file_reference, handle_failure=True):
    try:
        #TODO set config
        root_directory = PosixPath(config.STORAGE_DIRECTORY_PATH) / LOCAL_FILES_FOLDER
        file_handler = FileHandler(root_directory=root_directory, filename=filename)
        response = client.profile.parsing.add_file(source_key=source_key, reference=file_reference,
                                                    profile_file=file_handler.read_file(), created_at=file_handler.created_at)

        if not re.match(r"20[0-2]", str(response["code"])):
            if handle_failure:
                filepath = PosixPath(config.STORAGE_DIRECTORY_PATH) / LOCAL_FILES_FOLDER / filename # TODO better handle this
                failure_directory_path = PosixPath(config.STORAGE_DIRECTORY_PATH) / LOCAL_FAILURES_FOLDER 
                shutil.copy(filepath, failure_directory_path)
            return "Failure"
        return "Success"

    except Exception as e:
        if handle_failure:
            filepath = PosixPath(config.STORAGE_DIRECTORY_PATH) / LOCAL_FILES_FOLDER / filename # TODO better handle this
            failure_directory_path = PosixPath(config.STORAGE_DIRECTORY_PATH) / LOCAL_FAILURES_FOLDER 
            shutil.copy(filepath, failure_directory_path)
        return e.__class__.__name__


def send_batch_to_hrflow(
    client,
    source_key,
    filename_list,
    file_reference_list,
    multiprocess: typing.Optional[int] = 0,
    sleep_period: typing.Optional[int] = 6,
    max_workers: typing.Optional[int] = None,
) -> Counter:
    results = Counter()
    if multiprocess:
        with tqdm(
            total=len(filename_list), leave=False, desc="{:<30}".format("Sending Items to HrFlow"),
        ) as progress_bar:
            with ProcessPoolExecutor(
                max_workers=max_workers,
            ) as executor:
                futures = [
                    executor.submit(send_file_to_hrflow, client, source_key, filename, file_reference)
                    for filename, file_reference in zip(filename_list, file_reference_list)
                ]
                for finished in as_completed(futures):
                    progress_bar.update(1)
                    results[finished.result()] += 1
    else:
        with tqdm(
            total=len(filename_list), leave=False, desc="{:<30}".format("Sending Items to HrFlow"),
        ) as progress_bar:
            for filename, file_reference in zip(filename_list, file_reference_list):
                progress_bar.set_description("Importing...")
                result = send_file_to_hrflow(client, source_key, filename, file_reference)
                progress_bar.set_description(f"Pause for {sleep_period} secs...")
                time.sleep(sleep_period)
                progress_bar.update(1)
                results[result] += 1
                
    return results

