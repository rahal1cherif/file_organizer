
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from organizer import get_file_type, move_file_to_type_folder, move_categorize_file


class MockPath(Path):
    _flavour = Path('.')._flavour
    __slots__ = ('path',)

    def __new__(cls, *args, **kwargs):
        return super(Path, cls).__new__(cls, *args, **kwargs)

    def __init__(self, path):
        self.path = path

    def __truediv__(self, other):
        return MockPath(f"{self.path}/{other}")

    def __str__(self):
        return self.path

    def is_file(self):
        return True


class TestOrganizer (unittest.TestCase):

    def test_get_file_type_known_extensions(self):
        self.assertEqual(get_file_type(".mp4"), "Video")
        self.assertEqual(get_file_type(".mp3"), "Audio")
        self.assertEqual(get_file_type(".docx"), "Document")

    def test_get_file_type_unknown_extensions(self):
        self.assertIsNone(get_file_type("Unknown"))

    def test_get_file_type_case_sensitivity(self):
        self.assertEqual(get_file_type(".JPEG"), "Image")
        self.assertEqual(get_file_type(".CSV"), "Data")

    def mock_get_file_type_side_effect(file_extension):
        if file_extension == ".mp3":
            return "Audio"
        elif file_extension == ".pdf":
            return "Document"
        elif file_extension == ".mp4":
            return "Video"
        else:
            return "TestType"  # Default case

    @patch("organizer.Path.replace")
    @patch("organizer.Path.mkdir")
    # we assume the file does not exist in dir to trigger a move
    @patch("organizer.Path.exists", return_value=False)
    def test_move_file_to_type_folder(self, mock_exists, mock_mkdir,  mock_replace):

        move_file_to_type_folder(Path("test_audio.mp3"), "Audio")

        # check if the neccessary methods were called during a file move
        mock_mkdir.assert_called_once()
        mock_replace.assert_called_once()
        mock_exists.assert_called_once()

    @patch("organizer.move_file_to_type_folder")
    @patch("organizer.Path.rglob")
    @patch("organizer.get_file_type", side_effect=mock_get_file_type_side_effect)
    @patch("organizer.FOLDER_PATH", new_callable=MagicMock)
    def test_move_categorize_file(self, mock_folder_path, mock_get_file_type, mock_rglob, mock_move_file_to_type_folder):
        folder_path = MockPath("/test")  
        mock_rglob.return_value = [
            folder_path / "test_audio.mp3",
            folder_path / "document.pdf",
            folder_path / "video.mp4"
        ]
        mock_folder_path.__str__.return_value = str(folder_path)

        print("folder_path:", folder_path)
        mock_get_file_type(folder_path)
        move_categorize_file(folder_path)

        print("mock_move_file_to_type_folder.call_count:",
              mock_move_file_to_type_folder.call_count)
        print("mock_move_file_to_type_folder.call_args_list:",
              mock_move_file_to_type_folder.call_args_list)

        # check if the function is called for each file type
        self.assertEqual(mock_move_file_to_type_folder.call_count, 3)
        mock_move_file_to_type_folder.assert_any_call(
            folder_path / "test_audio.mp3", "Audio")
        mock_move_file_to_type_folder.assert_any_call(
            folder_path / "document.pdf", "Document")
        mock_move_file_to_type_folder.assert_any_call(
            folder_path / "video.mp4", "Video")


if __name__ == "__main__":
    unittest.main()
