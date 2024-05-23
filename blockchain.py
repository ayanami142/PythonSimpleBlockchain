import hashlib
import time


class Block:
    def __init__(
            self,
            index: int,
            previous_hash: str,
            transactions: str,
            timestamp: float | None = None,
            nonce: int = 0
    ) -> None:
        """
        Initialize a new block.
        :index: int - The position of the block in the blockchain.
        :param previous_hash: str - The hash of the previous block in the chain.
        :param transactions: str - The transactions included in the block.
        :param timestamp: float | optional - The time the block was created. Defaults to the current time.
        :param nonce: int | optional - The nonce used for the proof-of-work algorithm. Defaults to 0.
        :return: None
        """
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the SHA-256 hash of the block.
        :return: str - The hash of the block.
        """
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Perform the proof-of-work algorithm to mine the block.
        :param difficulty: int - The difficulty level for the proof-of-work algorithm,
            represented by the number of leading zeros required in the hash.
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self) -> str:
        """
        Return a string representation of the block.
        :return: str - A string representation of the block.
        """
        return (f"Block(Index: {self.index}, "
                f"Previous Hash: {self.previous_hash}, "
                f"Transactions: {self.transactions}, "
                f"Timestamp: {self.timestamp}, "
                f"Nonce: {self.nonce}, "
                f"Hash: {self.hash})")


class BlockChain:
    def __init__(self, difficulty: int = 6) -> None:
        """
        Initializes a new instance of the BlockChain class.
        :param difficulty (int, optional):
             Difficulty level for mining blocks. Defaults to 6.
                The higher the difficulty, the more computational
                effort required to mine a block.
        :return: None
        """
        self.chain = [BlockChain.create_genesis_block()]
        self.difficulty = difficulty

    @staticmethod
    def create_genesis_block() -> Block:
        """
        Create a Block instance with 0 values as the first block in the chain
        :return: Block - Block instance
        """
        return Block(0, "0", "Genesis Block")

    def get_latest_block(self) -> Block:
        """
        Get the latest block from the chain
        :return: Block - Latest Block instance
        """
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """
        Add new block to the chain and mine this before adding
        :param new_block: Block instance
        :return: None
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """
        return False if current block 's previous hash is not equal to previous,
        or current block 's hash doesn't equal to calculated hash,
        or mined hash doesn't equal to current block's hash
        else return True
        :return: bool - is chain valid or not
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if (
                    current_block.hash != current_block.calculate_hash() or
                    previous_block.hash != current_block.previous_hash or
                    not current_block.hash.startswith('0' * self.difficulty)
            ):
                return False
        return True

    def calculate_index(self) -> int:
        """
        Get the latest block's index and increment it
        :return: int - calculated index for the block
        """
        return self.get_latest_block().index + 1

    def __repr__(self) -> str:
        """
        Generate list of blocks in the chain and join them as a string
        :return: str - joined list of strings with the blocks
        """
        return "\n".join([str(block) for block in self.chain])
