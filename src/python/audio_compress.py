import pexpect
import signal
import os
import tempfile
import click
import shutil

from utilities.dependency import check_dependencies
from utilities.prompt import ask_file, select_from_list, exit_with_message, ask_number


signal.signal(signal.SIGINT, signal.SIG_DFL)
check_dependencies(["ffmpeg", "split", "gum", "fd", "fzf"])


def select_bit() -> str:
    bits = ["16k", "32k", "64k", "128k", "256k", "320k"]
    selected_bits = select_from_list(bits, 1)
    if not selected_bits:
        exit_with_message("You didn't select a bitrate")

    return selected_bits[0]


def escape_path(path: str) -> str:
    return path.replace(" ", "\\ ")


# (/Desktop, "foo") -> mac: /Desktop/foo, windows: \Desktop\foo
# (/Desktop/foo, "bar") -> mac: /Desktop/foo/bar, windows: \Desktop\foo\bar
def get_os_specific_path(args: list[str]) -> str:
    return os.path.join(*args)


def split_to_part(temp_dir: tempfile.TemporaryDirectory, file_name_without_ext: str, file_to_split: str, max_mb: int):
    part_path = escape_path(get_os_specific_path(
        [temp_dir.name, f"{file_name_without_ext}_part_"]))
    split_cmd = f"""split -b {max_mb}M {escape_path(file_to_split)} {part_path}"""
    child = pexpect.spawn(split_cmd, timeout=600, encoding='utf-8')
    child.expect(pexpect.EOF)


def convert_part_to_mp3(temp_dir: tempfile.TemporaryDirectory, file_name_without_ext: str):
    for part_file in os.listdir(temp_dir.name):
        full_path = get_os_specific_path([temp_dir.name, part_file])
        cmd = f"""ffmpeg -i {escape_path(full_path)} -c:a copy {escape_path(full_path)}.mp3"""
        child = pexpect.spawn(cmd, timeout=600, encoding='utf-8')
        child.expect(pexpect.EOF)
        os.remove(full_path)

    # copy everything from that temp dir to a new dir in the original mp3 file
    # create compress dir if it doesn't exist
    if not os.path.isdir("compressed"):
        os.makedirs("compressed")

    # delete dir if exists
    if os.path.isdir(get_os_specific_path(["compressed", file_name_without_ext])):
        shutil.rmtree(get_os_specific_path(
            ["compressed", file_name_without_ext]))

    shutil.copytree(temp_dir.name, get_os_specific_path(
        ["compressed", file_name_without_ext]))


def compress(original_file_path: str, file_name_without_ext: str, bit: str) -> str:
    compress_path = f"{file_name_without_ext}_compressed_{bit}.mp3"
    compress_cmd = f"""ffmpeg -i {escape_path(original_file_path)} -map 0:a:0 -b:a {bit} {escape_path(compress_path)} -y"""

    child = pexpect.spawn(compress_cmd, timeout=600, encoding='utf-8')
    child.expect(pexpect.EOF)
    return compress_path


def exec(original_file_path: str, bit: str, max_mb: int):
    os.chdir(os.path.dirname(original_file_path))
    temp_dir = tempfile.TemporaryDirectory()
    file_name = None
    file_name_without_ext = ""

    file_name = os.path.basename(original_file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]

    compress_path = compress(original_file_path, file_name_without_ext, bit)

    split_to_part(temp_dir, file_name_without_ext, compress_path, max_mb)
    convert_part_to_mp3(temp_dir, file_name_without_ext)


@click.command()
@click.argument('files', required=False, nargs=-1, type=click.Path(exists=True))
def main(files: str):
    selected_files = list(files)

    if not selected_files:
        selected_files = ask_file(".", "fd | fzf")

    if not selected_files:
        exit_with_message("You didn't select any files")

    bit = select_bit()
    max_mb = ask_number("What is the max file size in MB?")

    for file in selected_files:
        print(file)
        exec(file, bit, max_mb)


if __name__ == "__main__":
    main()
