import unittest
from unittest.mock import patch, mock_open
import subprocess
import csv
import os
from hw2 import read_config, get_commit_tree, generate_graphviz_code, write_output


class TestGitCommitProcessor(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="repo_path,output_path\n/path/to/repo,/path/to/output"))
    def test_read_config(self):
        config = read_config("config.csv")
        self.assertEqual(config['repo_path'], '/path/to/repo')
        self.assertEqual(config['output_path'], '/path/to/output')

    @patch("subprocess.run")
    def test_get_commit_tree_success(self, mock_subprocess_run):
        # Mocking the subprocess run to simulate git log output
        mock_subprocess_run.return_value.returncode = 0
        mock_subprocess_run.return_value.stdout = "abc123 Commit message 1\ndef456 Commit message 2"
        mock_subprocess_run.return_value.stderr = ""

        commit_info = get_commit_tree("/path/to/repo")
        
        # Assert that commit_info is correctly parsed
        self.assertEqual(len(commit_info), 2)
        self.assertIn("abc123", commit_info)
        self.assertEqual(commit_info["abc123"]['message'], "Commit message 1")
        self.assertIn("def456", commit_info)
        self.assertEqual(commit_info["def456"]['message'], "Commit message 2")
    
    @patch("subprocess.run")
    def test_get_commit_tree_failure(self, mock_subprocess_run):
        # Simulate a failure in subprocess
        mock_subprocess_run.return_value.returncode = 1
        mock_subprocess_run.return_value.stderr = "Error: Git command failed"
        
        commit_info = get_commit_tree("/path/to/repo")
        
        # Assert that commit_info is empty
        self.assertEqual(commit_info, {})
    
    def test_generate_graphviz_code(self):
        # A sample commit info structure
        commit_info = {
            "abc123": {"message": "Commit message 1", "children": []},
            "def456": {"message": "Commit message 2", "children": []},
        }
        
        # Generate Graphviz code
        graphviz_code = generate_graphviz_code(commit_info)
        
        # Check if the output contains expected parts of the graph
        self.assertIn('"abc123" [label="Commit message 1\\n+ abc123", shape=box]', graphviz_code)
        self.assertIn('"def456" [label="Commit message 2\\n+ def456", shape=box]', graphviz_code)
        self.assertIn('"abc123" -> "def456"', graphviz_code)

    @patch("builtins.open", mock_open())
    def test_write_output(self):
        content = "graphviz code"
        write_output("/path/to/output", content)
        
        # Ensure that the output file is being written with the expected content
        with open("/path/to/output", 'w') as f:
            f.write(content)
        # Verify if the write method was called with the correct arguments
        open.assert_called_with("/path/to/output", 'w')


if __name__ == "__main__":
    unittest.main()
