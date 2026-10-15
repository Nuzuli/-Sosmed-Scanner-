import sys
import pytest
from unittest.mock import patch
from sosmed_scanner.cli import main

def test_cli_missing_arguments():
    """Menguji apakah sistem keluar dengan kode 1 jika argumen kosong."""
    with patch.object(sys, 'argv', ['cli.py']):
        with pytest.raises(SystemExit) as sample_error:
            main()
        assert sample_error.value.code == 1

def test_cli_invalid_username_regex(caplog):
    """Menguji apakah sistem menolak username dengan karakter ilegal."""
    with patch.object(sys, 'argv', ['cli.py', 'user!@#invalid']):
        with pytest.raises(SystemExit) as sample_error:
            main()
        assert sample_error.value.code == 1
        assert "Input tidak valid" in caplog.text

@patch('sosmed_scanner.cli.jalankan_pencarian')
def test_cli_happy_path(mock_jalankan):
    """Menguji jalur sukses jika input username sudah sesuai aturan."""
    with patch.object(sys, 'argv', ['cli.py', 'valid.user_123']):
        main()
        mock_jalankan.assert_called_once_with('valid.user_123')
