import unittest
from scrapper.data_parser import LotteryGame, LotteryResultsCollector

class TestDataParser(unittest.TestCase):
    def test_lottery_game_init(self):
        game = LotteryGame(table='lotto', id='123', nums1='1,2,3', date='2023-07-25', time='1234')
        self.assertEqual(game.table, 'lotto')
        self.assertEqual(game.id, '123')
        self.assertEqual(game.nums1, '1,2,3')
        self.assertEqual(game.date, '2023-07-25')
        self.assertEqual(game.time, '1234')

    def test_lottery_results_collector(self):
        collector = LotteryResultsCollector()
        self.assertEqual(len(collector.results), 0)
        game1 = LotteryGame(table='lotto', id='123', nums1='1,2,3', date='2023-07-25', time='1234')
        game2 = LotteryGame(table='eurojackpot', id='456', nums1='4,5,6', date='2023-07-26', time='2345')
        collector.add_result(game1)
        collector.add_result(game2)

        self.assertEqual(len(collector.results), 2)

if __name__ == '__main__':
    unittest.main()
