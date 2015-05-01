# -*- coding: UTF-8-*-

import odoj_parser as parser

class Member(object):
	"""model for an ODOJ group member"""
	def __init__(self, name_location, points):
		self.name_location = name_location
		self.name = parser.get_name_only(name_location)
		self.points = points
		average = sum(points)/float(len(points))
		self.average = round(average, 2)
		self.percentage = round(average/3*100,2)

	def print_weekly_point(self):
		return '{0} {1}%'.format(self.name, '💯' if self.percentage >= 100 else str(self.percentage))

class RankClass(object):
	"""model for class of weekly achievement
	(kelas/group index prestsi pekanan)"""
	def __init__(self, raw_header):
		minimum,maximum = parser.get_class_minmax(raw_header)
		self.raw_header = raw_header
		self.minimum = minimum
		self.maximum = maximum
		self.member = []

	def print_class(self, show_header=False):
		result = 'TIDAK ADA/NONE\n'
		if len(self.member)>0:
			result = '\n'.join(map(lambda x: x.print_weekly_point(), self.member)) + '\n'
		if show_header:
			result = 'Class {0}:\n'.format(self.raw_header) + result
		return result + '\n'

	def insertTo(self, template):
		result = parser.insert_members_line(self.print_class(), template, self.raw_header)
		return result

class WeeklyReport(object):
	"""model for ODOJ Group's weekly report"""
	def __init__(self, raw, template):
		self.raw = raw
		self.template = parser.clean_template(template)
		self.member = {}
		self.classes = []
		member_names = parser.get_member_names(raw)
		for name in member_names:
			points = parser.get_daily_point(raw, name)
			member = Member(name, points)
			self.member[member.name] = member

		classes = parser.get_classes_range(template)
		member_ordered = self.get_sorted_data()
		for c in classes:
			minimum,maximum = parser.get_class_minmax(c)
			rank_class = RankClass(c)
			for m in member_ordered:
				if m.percentage >= rank_class.minimum and m.percentage <= rank_class.maximum:
					rank_class.member.append(m)
			self.classes.append(rank_class)

	def get_sorted_data(self):
		return sorted(self.member.itervalues(), key=lambda x: x.average, reverse=True)

	def print_raw(self):
		return '\n'.join(map(lambda x: x.print_weekly_point(), self.get_sorted_data()))

	def populate_template(self):
		result = self.template
		result = parser.update_edition(result)
		for c in self.classes:
			result = c.insertTo(result)
		return result

	def print_classified(self, template=False):
		if not template:
			return '\n'.join(map(lambda x: x.print_class(show_header=True), self.classes))
		else:
			return self.populate_template()

