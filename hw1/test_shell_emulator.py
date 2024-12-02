import pytest
import os
from main import execute_command, extract_virtual_fs

@pytest.fixture
def setup_environment(tmpdir):

    zip_path = "D:/conf1/shell_emulator2/virtual_fs.zip"

    extract_virtual_fs(zip_path)
    virtual_fs_path = os.path.join(tmpdir, "virtual_fs")
    os.makedirs(virtual_fs_path, exist_ok=True)
    
    return virtual_fs_path

def test_cd_to_nonexistent_directory(setup_environment):
    current_dir = setup_environment
    root_dir = setup_environment
    result = execute_command("cd nonexistent", current_dir, root_dir)
    assert "Error: nonexistent is not a directory." in result

def test_cd_with_multiple_dots(setup_environment):
    current_dir = setup_environment
    root_dir = setup_environment
    result = execute_command("cd .....", current_dir, root_dir)
    assert "Error:" in result

def test_unknown_command(setup_environment):
    current_dir = setup_environment
    root_dir = setup_environment
    result = execute_command("cdgioejrgioe", current_dir, root_dir)
    assert "Unknown command" in result

def test_cd_with_spaces(setup_environment):
    current_dir = setup_environment
    root_dir = setup_environment
    result = execute_command("cd    ", current_dir, root_dir)
    assert "Error: 'cd' requires a target directory." in result

def test_rm_nonexistent_file(setup_environment):
    current_dir = setup_environment
    root_dir = setup_environment
    result = execute_command("rm nonexistent_file", current_dir, root_dir)
    assert "Error: nonexistent_file does not exist." in result

