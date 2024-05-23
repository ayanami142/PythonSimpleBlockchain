import hashlib
import time


class Block:
    def __init__(self, index: int, previous_hash: str, transactions: str, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self):
        return (f"Block(Index: {self.index}, "
                f"Previous Hash: {self.previous_hash}, "
                f"Transactions: {self.transactions}, "
                f"Timestamp: {self.timestamp}, "
                f"Nonce: {self.nonce}, "
                f"Hash: {self.hash})")


class BlockChain:
    def __init__(self, difficulty=1):
        self.chain = [BlockChain.create_genesis_block()]
        self.difficulty = difficulty

    @staticmethod
    def create_genesis_block():
        return Block(0, "0", "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        print('added new block = ', new_block)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if previous_block.hash != current_block.previous_hash:
                return False
            if not current_block.hash.startswith('0' * self.difficulty):
                return False
        return True

    def calculate_index(self):
        return self.get_latest_block().index + 1

    def __repr__(self):
        return "\n".join([str(block) for block in self.chain])
