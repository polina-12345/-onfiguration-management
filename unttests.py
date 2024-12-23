import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import tkinter as tk
from emulator import ShellEmulator 


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.emulator = ShellEmulator(self.root, "virtual_fs.tar")

    @patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
    def test_list_files(self, mock_listdir):
        self.emulator.current_path = "/"  # Установим текущую директорию
        self.emulator.list_files()
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    @patch('os.path.isdir', return_value=True)
    def test_change_directory(self, mock_isdir):
        self.emulator.change_directory("subdir")
        self.assertEqual(self.emulator.current_path, "subdir")

    @patch('os.path.isdir', return_value=False)
    def test_change_directory_not_found(self, mock_isdir):
        self.emulator.change_directory("nonexistent")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("Директория не найдена", output)

    def test_print_working_directory(self):
        self.emulator.print_working_directory()
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn(f"{self.emulator.username}:/", output)

    @patch('builtins.open', new_callable=mock_open, read_data="file content")
    def test_copy_file(self, mock_file):
        # Подготовка
        self.emulator.current_path = "/"
        
        # Тестирование успешного копирования файла
        self.emulator.copy_file("file1.txt file2.txt")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("Файл или директория не найдены.\n\n", output)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_copy_file_not_found(self, mock_file):
        # Подготовка
        self.emulator.current_path = "/"
        
        # Тестирование неудачного копирования файла
        self.emulator.copy_file("nonexistent.txt destination.txt")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("Файл или директория не найдены.", output)

    def test_show_calendar(self):
        with patch('calendar.month', return_value="December 2024\nMo Tu We Th Fr Sa Su\n       1  2  3  4  5  6  7\n8  9 10 11 12 13 14\n15 16 17 18 19 20 21\n22 23 24 25 26 27 28\n29 30 31"):
            self.emulator.show_calendar()
            output = self.emulator.text_area.get("1.0", tk.END)
            self.assertIn("December 2024", output)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
