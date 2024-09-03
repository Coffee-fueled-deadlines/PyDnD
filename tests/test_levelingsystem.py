import unittest
from unittest.mock import MagicMock

from PyDnD.LevelingSystem import LevelingSystem
from PyDnD.Player import Player

class TestLevelingSystem(unittest.TestCase):

    def setUp(self):
        """Set up a basic player and leveling system for testing."""
        self.player = Player(name="Test Player", level=1)
        self.leveling_system = LevelingSystem(self.player)

    def test_initial_experience(self):
        """Test that the player starts with the correct initial experience."""
        self.assertEqual(self.player.experience, 0, "Initial experience should be 0 at level 1")

    def test_give_experience_level_up(self):
        """Test that giving experience correctly levels up the player."""
        self.leveling_system.giveExp(1000)
        self.assertEqual(self.player.level, 2, "Player should level up to 2 after gaining 1000 XP")
        self.assertEqual(self.player.experience, 1000, "Player's experience should be 1000 after leveling up")
        self.assertEqual(self.leveling_system.nextLvlExperience, 3000 - 1000, "Next level experience should be correctly calculated")

    def test_remove_experience_level_down(self):
        """Test that removing experience correctly levels down the player."""
        self.leveling_system.giveExp(3000)
        self.assertEqual(self.player.level, 3, "Player should level up to 3 after gaining 3000 XP")
        
        self.leveling_system.removeExp(2000)
        self.assertEqual(self.player.level, 2, "Player should level down to 2 after losing 2000 XP")
        self.assertEqual(self.player.experience, 1000, "Player's experience should be 1000 after leveling down")
        self.assertEqual(self.leveling_system.nextLvlExperience, 3000 - 1000, "Next level experience should be correctly calculated for level 2")

    def test_no_level_down_below_1(self):
        """Test that the player does not level down below level 1."""
        self.leveling_system.giveExp(500)
        self.leveling_system.removeExp(1000)
        self.assertEqual(self.player.level, 1, "Player should not level down below 1")
        self.assertEqual(self.player.experience, 0, "Player's experience should be 0 after losing all XP")

    def test_get_threshold_for_next_level(self):
        """Test calculation of the experience threshold for the next level."""
        threshold = self.leveling_system.getThresholdForNextLevel()
        expected_threshold = int(1000 * (2 + LevelingSystem.nCr(2, 2)) - 2 * 1000)
        self.assertEqual(threshold, expected_threshold, "Threshold for next level should be correctly calculated")

    def test_get_threshold_for_current_level(self):
        """Test calculation of the experience threshold for the current level."""
        threshold = self.leveling_system.getThresholdForCurrentLevel()
        expected_threshold = int(1000 * (1 + LevelingSystem.nCr(1, 2)) - 1 * 1000)
        self.assertEqual(threshold, expected_threshold, "Threshold for current level should be correctly calculated")

    def test_invalid_nCr(self):
        """Test that nCr calculation handles invalid inputs."""
        self.assertEqual(LevelingSystem.nCr(5, 0), 1.0, "nCr with r=0 should be 1.0")
        self.assertEqual(LevelingSystem.nCr(5, 5), 1.0, "nCr with r=n should be 1.0")
        self.assertEqual(LevelingSystem.nCr(5, 3), 10.0, "nCr should correctly calculate the combinations")

if __name__ == '__main__':
    unittest.main()
