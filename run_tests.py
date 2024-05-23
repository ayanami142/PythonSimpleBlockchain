from unittest import TestLoader, TextTestRunner

from tests.test_block import TestBlock
from tests.test_blockchain import TestBlockChain

if __name__ == '__main__':
    test_suite = TestLoader().loadTestsFromTestCase(TestBlock)
    test_suite.addTests(TestLoader().loadTestsFromTestCase(TestBlockChain))
    TextTestRunner().run(test_suite)
