import os
import subprocess
import sys
import pytest
from git_dep import load_config, get_commits_from_repo, escape_graphviz_string, generate_graphviz_tree, visualize_graph

# Тесты для функции load_config
def test_load_config_valid():
    args = ["script_name", "repo_path", "dot_path"]
    config = load_config(args)
    assert config == {"repository_path": "repo_path", "visualization_program_path": "dot_path"}

def test_load_config_invalid():
    args = ["script_name", "repo_path"]
    with pytest.raises(ValueError):
        load_config(args)

# Тесты для функции get_commits_from_repo
def test_get_commits_from_repo(mocker):
    mocker.patch("subprocess.run", return_value=subprocess.CompletedProcess(
        args=[], returncode=0, stdout="hash1;parent1 parent2;message1\nhash2;parent1;message2"
    ))
    commits = get_commits_from_repo("repo_path")
    assert commits == {
        "hash1": {"parents": ["parent1", "parent2"], "message": "message1"},
        "hash2": {"parents": ["parent1"], "message": "message2"}
    }

def test_get_commits_from_repo_error(mocker):
    mocker.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "git"))
    commits = get_commits_from_repo("repo_path")
    assert commits == {}

# Тесты для функции escape_graphviz_string
def test_escape_graphviz_string():
    assert escape_graphviz_string('Hello "World" \\') == 'Hello \\"World\\" \\\\'

# Тесты для функции generate_graphviz_tree
def test_generate_graphviz_tree(tmpdir):
    commits = {
        "hash1": {"parents": ["parent1", "parent2"], "message": "message1"},
        "hash2": {"parents": ["parent1"], "message": "message2"}
    }
    output_file_path = tmpdir.join("test.gv")
    generate_graphviz_tree(commits, output_file_path)
    with open(output_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert 'digraph G {' in content
    assert '"hash1" [label="message1"];' in content
    assert '"parent1" -> "hash1";' in content

# Тесты для функции visualize_graph
def test_visualize_graph(mocker, tmpdir):
    mocker.patch("subprocess.run")
    mocker.patch("os.startfile")
    graphviz_path = "dot"
    input_file_path = "test.gv"
    output_image_path = tmpdir.join("test.png")
    visualize_graph(graphviz_path, input_file_path, output_image_path)
    subprocess.run.assert_called_once_with(["dot", "-Tpng", "-o", str(output_image_path), "test.gv"], check=True)
    os.startfile.assert_called_once_with(str(output_image_path))
