import unittest
from datetime import datetime
import file_utils as utils
import odoj_parser as ip_gen



def is_lists_equal(list1, list2):
    return len(list1) == len(list2) and sorted(list1) == sorted(list2)

class TestParser(unittest.TestCase):
    # """test package for odoj 'index prestasi pekanan' generator"""

    def setUp(self):
        self.sample_rekap_akhir_pekan = utils.read_file('rekap_harian.txt')
        self.sample_rekap_ip = utils.read_file('rekap_pekanan.txt')


    def test_get_member_names(self):
        member_names = ip_gen.get_member_names(self.sample_rekap_akhir_pekan)
        # with open(test_files_dir+os.sep+'rekap_harian_test.txt', 'w') as f:
        #     for data in result:
        #         f.write(data + '\r\n')

        self.assertEqual(len(member_names), 30) #result sesuai jml member group = 30 orang

    def test_get_daily_point(self):
        member_names = ip_gen.get_member_names(self.sample_rekap_akhir_pekan)

        zainul = ip_gen.get_daily_point(self.sample_rekap_akhir_pekan, member_names[0])
        musab = ip_gen.get_daily_point(self.sample_rekap_akhir_pekan, member_names[13])
        arjuna = ip_gen.get_daily_point(self.sample_rekap_akhir_pekan, member_names[6])
        syahri = ip_gen.get_daily_point(self.sample_rekap_akhir_pekan, member_names[23])
        sopian = ip_gen.get_daily_point(self.sample_rekap_akhir_pekan, member_names[29])

        self.assertTrue(is_lists_equal(zainul, [1,3,1,0,0,0,0]))
        self.assertTrue(is_lists_equal(musab, [3,2,3,0,0,0,0]))
        self.assertTrue(is_lists_equal(arjuna, [1,0,1,0,0,0,0]))
        self.assertTrue(is_lists_equal(syahri, [1,0,1,0,0,0,0]))
        self.assertTrue(is_lists_equal(sopian, [2,2,3,3,0,0,0]))

    def test_int_with_default(self):
        self.assertEqual(ip_gen.convert('1000'),1000)
        self.assertEqual(ip_gen.convert('3'),3)
        self.assertEqual(ip_gen.convert('x'),0)
        self.assertEqual(ip_gen.convert('0'),0)
        self.assertEqual(ip_gen.convert('z'),0)

    def test_get_name_only(self):
        self.assertEqual(ip_gen.get_name_only('azwar_padang'), 'azwar')
        self.assertEqual(ip_gen.get_name_only("mus'ab_UK"), "mus'ab")
        self.assertEqual(ip_gen.get_name_only('foo'), 'foo')
        self.assertEqual(ip_gen.get_name_only('_bar'), '')

    def test_get_class_minmax(self):
        text = ['(86-100)','(70,00-85,99)','(10-33,99)']
        expected = [(86,100), (70,85.99),(10,33.99)]
        for i in range(len(text)):
            actual = ip_gen.get_class_minmax(text[i])
            self.assertEqual(expected[i], actual)

    def test_update_edition(self):
        template = """Edisi 5-11April 2015
Member Teladan (86-100)
===================
Ali Rosyadi """
        expected = """Edisi 19-25 April 2015
Member Teladan (86-100)
===================
Ali Rosyadi """
        template = ip_gen.update_edition(template, datetime(2015,4,25,0,0))
        self.assertEqual(template, expected)

    def test_insert_members_line(self):
        template = """Member  Teladan (86-100)
===================
Yudhis 95,2%
Rohmat 90,5%
Fuja 90,5%
MEMBER Unggulan (70,00-85,99)
==============="""
        expected = """Member  Teladan (86-100)
===================
Gustie 90%
Hanif 87%
Asep 86%
MEMBER Unggulan (70,00-85,99)
==============="""
        members = """Gustie 90%
Hanif 87%
Asep 86%
"""
        raw_header = "(86-100)"
        template = ip_gen.clean_template(template)
        template = ip_gen.insert_members_line(members, template, raw_header)
        self.assertEqual(template, expected)

    def test_get_classes_range(self):
        expected = ['(86-100)','(70,00-85,99)','(50-69,99)','(34-49,99)','(10-33,99)']
        actual = ip_gen.get_classes_range(self.sample_rekap_ip)
        self.assertTrue(is_lists_equal(expected, actual))

        template = """Member  Teladan (100)
===================
Some body 100%
MEMBER Unggulan (Jangan di match 70,00-85,99)
==============="""
        expected = ["(100)"]
        actual = ip_gen.get_classes_range(template)
        self.assertTrue(is_lists_equal(expected, actual))

    def test_clean_template(self):
        #remove member name line (including new line character)
        self.assertEqual(ip_gen.clean_template("Yudhis 95,2%"), "")
        template = """Yudhis 95,2%
"""
        self.assertEqual(ip_gen.clean_template(template), "")
        template = """Member  Teladan (86-100)
===================
Yudhis 95,2%
Rohmat 90,5%
Fuja 90,5%
MEMBER Unggulan (70,00-85,99)
==============="""
        result = """Member  Teladan (86-100)
===================
MEMBER Unggulan (70,00-85,99)
==============="""
        self.assertEqual(ip_gen.clean_template(template), result)






if __name__ == '__main__':
    unittest.main()
