# for development and testing only
# provide functionality, data types etc. that will be later moved to the workflow code
from __future__ import annotations

from pathlib import Path
import os
from typing import Optional
import tarfile
import fnmatch
import shutil

from pyiron_workflow import Workflow


class Storage:
    def _convert_to_dict(instance):
        # Get the attributes of the instance
        attributes = vars(instance)

        # Convert attributes to a dictionary
        result_dict = {
            key: value for key, value in attributes.items() if "_" not in key[0]
        }

        return result_dict

class ShellOutput(Storage):
    stdout: str
    stderr: str
    return_code: int
    dump: FileObject  # TODO: should be done in a specific lammps object
    log: FileObject
    
class VarType:
    def __init__(
        self,
        value=None,
        dat_type=None,
        label: str = None,
        store: int = 0,
        generic: bool = None,
        doc: str = None,
    ):
        self.value = value
        self.type = dat_type
        self.label = label
        self.store = store
        self.generic = generic
        self.doc = doc


class FileObject:
    def __init__(self, path=".", directory=None):
        if directory is None:
            self._path = Path(path)
        else:
            self._path = Path(directory) / Path(path)

    def __repr__(self):
        return f"FileObject: {self._path} {self.is_file}"

    @property
    def path(self):
        # Note conversion to string (needed to satisfy glob which is used e.g. in dump parser)
        return str(self._path)

    @property
    def is_file(self):
        return self._path.is_file()

    @property
    def name(self):
        return self._path.name
    
@Workflow.wrap.as_function_node("output")#, "dump", "log")
def Shell(
        working_directory: str,
        command: str = "lmp",
        environment: Optional[dict] = None,
        arguments: Optional[list] = None,
):
    arguments = ["-in", "control.inp"] if arguments is None else arguments
    # -> (ShellOutput, FileObject, FileObject):  TODO: fails -> why
    import os
    import subprocess

    if environment is None:
        environment = {}
    if arguments is None:
        arguments = []

    environ = dict(os.environ)
    environ.update({k: str(v) for k, v in environment.items()})
    # print ([str(command), *map(str, arguments)], working_directory, environment)
    # print("start shell")
    proc = subprocess.run(
        [command, *map(str, arguments)],
        capture_output=True,
        cwd=working_directory,
        encoding="utf8",
        env=environ,
    )
    # print("end shell")

    output = ShellOutput()
    output.stdout = proc.stdout
    output.stderr = proc.stderr
    output.return_code = proc.returncode
    # dump = FileObject("dump.out", working_directory)
    # log = FileObject("log.lammps", working_directory)

    return output#, dump, log

@Workflow.wrap.as_function_node("workdir")
def delete_files_recursively(workdir: str, files_to_be_deleted: list[str]):
    """
    Recursively delete specific files in a directory and its subdirectories.

    Args:
        workdir (str): The directory to search for files.
        files_to_be_deleted (list[str]): List of filenames to delete.
    """
    if not os.path.isdir(workdir):
        print(f"Error: {workdir} is not a valid directory.")
    else:
        for root, _, files in os.walk(workdir):
            for file in files:
                if file in files_to_be_deleted:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
    return workdir

@Workflow.wrap.as_function_node("compressed_file")
def compress_directory(
    directory_path: str,
    exclude_files=[],
    exclude_file_patterns=[],
    print_message=True,
    inside_dir=True,
    actually_compress=True,
):
    """
    Compresses a directory and its contents into a tarball with gzip compression.

    Parameters:
        directory_path (str): The path of the directory to compress.
        exclude_files (list, optional): A list of filenames to exclude from the compression. Defaults to an empty list.
        exclude_file_patterns (list, optional): A list of file patterns (glob patterns) to match against filenames and exclude from the compression. Defaults to an empty list.
        print_message (bool, optional): Determines whether to print a message indicating the compression. Defaults to True.
        inside_dir (bool, optional): Determines whether the output tarball should be placed inside the source directory or in the same directory as the source directory. Defaults to True.

    Usage:
        # Compress a directory and place the resulting tarball inside the directory
        compress_directory("/path/to/source_directory")

        # Compress a directory and place the resulting tarball in the same directory as the source directory
        compress_directory("/path/to/source_directory", inside_dir=False)

        # Compress a directory and exclude specific files from the compression
        compress_directory("/path/to/source_directory", exclude_files=["file1.txt", "file2.jpg"])

        # Compress a directory and exclude files matching specific file patterns from the compression
        compress_directory("/path/to/source_directory", exclude_file_patterns=["*.txt", "*.log"], inside_dir=False)

    Note:
        - The function creates a tarball with gzip compression of the directory and its contents.
        - The resulting tarball will be placed either inside the source directory (if inside_dir is True) or in the same directory as the source directory (if inside_dir is False).
        - Files specified in the `exclude_files` list and those matching the `exclude_file_patterns` will be excluded from the compression.
        - The `print_message` parameter controls whether a message indicating the compression is printed. By default, it is set to True.
    """
    if actually_compress:
        if inside_dir:
            output_file = os.path.join(
                directory_path, os.path.basename(directory_path) + ".tar.gz"
            )
        else:
            output_file = os.path.join(
                os.path.dirname(directory_path),
                os.path.basename(directory_path) + ".tar.gz",
            )
        with tarfile.open(output_file, "w:gz") as tar:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Exclude the output tarball from being added
                    if file_path == output_file:
                        continue
                    if any(
                        fnmatch.fnmatch(file, pattern) for pattern in exclude_file_patterns
                    ):
                        continue
                    if file in exclude_files:
                        continue
                    arcname = os.path.join(
                        os.path.basename(directory_path),
                        os.path.relpath(file_path, directory_path),
                    )
                    tar.add(file_path, arcname=arcname)
                    # tar.add(file_path, arcname=os.path.relpath(file_path, directory_path))
                    # print(f"{file} added")
        if print_message:
            print(f"Compressed directory: {directory_path}")
    else:
        output_file = None
        print("no compression")
    return output_file

@Workflow.wrap.as_function_node("compressed_file")
def remove_dir(directory_path, actually_remove=False):
    if actually_remove:
        shutil.rmtree(directory_path, ignore_errors=True)
    return directory_path