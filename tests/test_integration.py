from unittest.mock import patch
from sosmed_scanner.scanner import jalankan_pencarian

def test_jalankan_pencarian_berjalan():
    with patch("sosmed_scanner.network.urlopen") as mock_urlopen:

        mock_urlopen.return_value.__enter__.return_value.status = 404
        hasil = jalankan_pencarian("username_tes123")
        assert len(hasil) == 3
