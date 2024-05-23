from unittest import TestCase

from blockchain import BlockChain, Block


class TestBlockChain(TestCase):
    def setUp(self):
        self.blockchain = BlockChain(difficulty=2)

    def test_genesis_block(self):
        genesis_block = self.blockchain.create_genesis_block()
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, "0")
        self.assertEqual(genesis_block.transactions, "Genesis Block")

    def test_add_block(self):
        initial_chain_length = len(self.blockchain.chain)
        new_block = Block(
            index=self.blockchain.calculate_index(),
            previous_hash=self.blockchain.get_latest_block().hash,
            transactions="New Block Data",
        )
        self.blockchain.add_block(new_block)
        self.assertEqual(len(self.blockchain.chain), initial_chain_length + 1)
        self.assertEqual(self.blockchain.get_latest_block(), new_block)

    def test_is_chain_valid(self):
        self.blockchain.add_block(Block(
            index=self.blockchain.calculate_index(),
            previous_hash=self.blockchain.get_latest_block().hash,
            transactions="Test Block 1"
        ))
        self.blockchain.add_block(Block(
            index=self.blockchain.calculate_index(),
            previous_hash=self.blockchain.get_latest_block().hash,
            transactions="Test Block 2"
        ))
        self.assertTrue(self.blockchain.is_chain_valid())

