from unittest import TestCase

from blockchain import Block


class TestBlock(TestCase):
    def setUp(self):
        self.index = 1
        self.previous_hash = "0" * 64
        self.transactions = "Test Transaction"
        self.block = Block(self.index, self.previous_hash, self.transactions)

    def test_block_creation(self):
        self.assertEqual(self.block.index, self.index)
        self.assertEqual(self.block.previous_hash, self.previous_hash)
        self.assertEqual(self.block.transactions, self.transactions)
        self.assertIsNotNone(self.block.timestamp)
        self.assertEqual(self.block.nonce, 0)

    def test_calculate_hash(self):
        expected_hash = self.block.calculate_hash()
        self.assertEqual(self.block.hash, expected_hash)

    def test_mine_block(self):
        difficulty = 2
        self.block.mine_block(difficulty)
        self.assertTrue(self.block.hash.startswith("0" * difficulty))
