import unittest
import file_utils as utils
from odoj_ip_generator import *


class TestWeeklyReport(unittest.TestCase):
    # """test package for odoj 'index prestasi pekanan' generator"""

    def setUp(self):
        self.weekly_report = WeeklyReport(utils.read_file('rekap_harian.txt'),utils.read_file('rekap_pekanan.txt'))

    def test_weekly_average(self):
    	#print self.weekly_report.member
        mawardi = 1.14
        self.assertEqual(self.weekly_report.member['mawardi'].average, mawardi)
        yudistira = 3
        self.assertEqual(self.weekly_report.member['yudistira'].average, yudistira)
        arjuna = 0.29
        self.assertEqual(self.weekly_report.member['arjuna'].average, arjuna)

    def test_weekly_raw(self):
        #print(self.weekly_report.print_raw())
        self.assertTrue(True)

    def test_weekly_classified(self):
        #print(self.weekly_report.print_classified())
        self.assertTrue(True)

    def test_weekly_classification(self):
        current_class = self.weekly_report.classes[0]
        maximum = 100.0
        minimum = 86.0
        class_member_names = map(lambda x: x.name, current_class.member)
        self.assertTrue('yudistira' in class_member_names)
        self.assertTrue(maximum==current_class.maximum)
        self.assertTrue(minimum==current_class.minimum)

        current_class = self.weekly_report.classes[3]
        minimum = 34.0
        maximum = 49.99
        class_member_names = map(lambda x: x.name, current_class.member)
        self.assertTrue('sopian' in class_member_names)
        self.assertTrue(maximum==current_class.maximum)
        self.assertTrue(minimum==current_class.minimum)


    def dont_use_test_get_weekly_point(self):
        member_names = ip_gen.get_member_names(self.sample_rekap_akhir_pekan)

        with open(test_files_dir+os.sep+'rekap_pekanan_test.txt', 'w') as f:
            for member in member_names:
                points = ip_gen.get_daily_point(self.sample_rekap_akhir_pekan, member)
                f.write(ip_gen.get_weekly_point(member, points) + '\r\n')

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
