import unittest
from src.sorting.anime import extract_subber, extract_title, extract_episode, extract_season, has_season, verify_no_season

anime1 = "[SubsPlease] Kimetsu no Yaiba - Hashira Geiko-hen - 04 (1080p) [0D0CBE3D].mkv"
anime2 = "[SubsPlease] Kono Subarashii Sekai ni Shukufuku wo! S3 - 015 (1080p) [D6088444].mkv"
anime3 = "[NeoLX] Tengoku Daimakyou (Heavenly Delusion) - S04E123 [720p x264 10bits AAC][Multiple Subtitles].mkv"

class TestAnimeExtractors(unittest.TestCase):

    def test_extract_subber(self):
        self.assertEqual(extract_subber(anime1), "SubsPlease")
        self.assertEqual(extract_subber(anime3), "NeoLX")
        with self.assertRaises(ValueError):
            extract_subber("Anime Title - 01 [720p].mkv")
        with self.assertRaises(ValueError):
            extract_subber("[Unknown] Anime Title - 01 [720p].mkv")

    def test_extract_title(self):
        self.assertEqual(extract_title(anime1), "Kimetsu no Yaiba - Hashira Geiko-hen")
        self.assertEqual(extract_title(anime2), "Kono Subarashii Sekai ni Shukufuku wo!")
        self.assertEqual(extract_title(anime3), "Tengoku Daimakyou (Heavenly Delusion) -")
        
        with self.assertRaises(ValueError):
            extract_subber("[Unknown] Anime Title - 01 [720p].mkv")
            
    def test_extract_episode(self):
        self.assertEqual(extract_episode(anime1), 4)
        self.assertEqual(extract_episode(anime2), 15)
        self.assertEqual(extract_episode(anime3), 123)
        
        with self.assertRaises(ValueError):
            extract_episode("[SubsPlease] Kono Subarashii Sekai ni Shukufuku wo! S3 -  (1080p) [D6088444].mkv")

    def test_extract_season(self):            
        self.assertEqual(extract_season(anime2), 3)
        self.assertEqual(extract_season(anime3), 4)
        
        with self.assertRaises(ValueError):
            extract_season(anime1)

    def test_has_season(self):
        self.assertFalse(has_season(anime1))
        self.assertTrue(has_season(anime2))
        self.assertTrue(has_season(anime3))

    def test_verify_no_season(self):
        self.assertTrue(verify_no_season(anime1))
        self.assertFalse(verify_no_season(anime2))
        self.assertFalse(verify_no_season(anime3))
