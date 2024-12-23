import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from hw2 import read_config, get_commit_tree, generate_graphviz_code, write_output, read_git_object, parse_commit_object
import zlib

class TestGitCommitProcessor(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="repo_path,output_path\n/path/to/repo,/path/to/output"))
    def test_read_config(self):
        config = read_config("config.csv")
        self.assertEqual(config['repo_path'], '/path/to/repo')
        self.assertEqual(config['output_path'], '/path/to/output')

    @patch("builtins.open", new_callable=mock_open, read_data="ref: refs/heads/main")
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    def test_read_git_object(self, mock_path_join, mock_isfile, mock_open_head):
        # Mock the git object file content
        compressed_data = zlib.compress(b"tree abcdef1234567890\nparent 123456abcdef7890\n\nCommit message")
        mock_open_head().read.return_value = compressed_data

        # Test the reading and parsing of a git object
        repo_path = "/path/to/repo"
        object_hash = "abcdef1234567890"
        result = read_git_object(repo_path, object_hash)

        self.assertIn("tree", result)
        self.assertIn("Commit message", result)

    def test_parse_commit_object(self):
        data = "tree abcdef1234567890\nparent 123456abcdef7890\n\nCommit message"
        tree, parents, message = parse_commit_object(data)

        self.assertEqual(tree, "abcdef1234567890")
        self.assertEqual(parents, ["123456abcdef7890"])
        self.assertEqual(message, "Commit message")

    @patch("builtins.open", new_callable=mock_open, read_data="ref: refs/heads/main")
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    def test_get_commit_tree(self, mock_path_join, mock_isfile, mock_open_head):
        # Mock the HEAD reference and the commit object files
        def side_effect_read(file, *args, **kwargs):
            if "refs/heads/main" in file:
                return mock_open(read_data="abcdef1234567890").return_value
            elif "abcdef1234567890" in file:
                return mock_open(read_data=zlib.compress(b"tree 123456abcdef7890\nparent 7890abcdef123456\n\nCommit message 1")).return_value
            elif "123456abcdef7890" in file:
                return mock_open(read_data=zlib.compress(b"tree 9876543210abcdef\n\nCommit message 2")).return_value

        mock_open_head.side_effect = side_effect_read


    def test_generate_graphviz_code(self):
        # A sample commit info structure
        commit_info = {
            "abc123": {"message": "Commit message 1", "parents": []},
            "def456": {"message": "Commit message 2", "parents": ["abc123"]},
        }

        # Generate Graphviz code
        graphviz_code = generate_graphviz_code(commit_info)

        # Check if the output contains expected parts of the graph
        self.assertIn('"abc123" [label="Commit message 1\\nabc123", shape=box]', graphviz_code)
        self.assertIn('"def456" [label="Commit message 2\\ndef456", shape=box]', graphviz_code)
        self.assertIn('"def456" -> "abc123"', graphviz_code)

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