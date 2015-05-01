# -*- coding: UTF-8-*-

import re
from datetime import datetime, timedelta

def convert(str):
	return int(str) if str.isdigit() else 0

def get_classes_range(text):
	#match at least : (integer_number)
	RANGE_RE = re.compile(r'\(\d+[.,]*\d*-*\d*[.,]*\d*\)', re.I|re.M)
	result = re.findall(RANGE_RE, text)
	return result

def get_class_minmax(class_range):
	#remove bracket () and replace comma with dot as standard decimal separator
	class_range = class_range.replace("(","").replace(")","").replace(",",".")
	minmax = class_range.split("-")
	minimum = float(minmax[0])
	maxiumm = minmax[1] if(len(minmax)>1) else minmax[0]
	maxiumm = float(maxiumm)
	return minimum, maxiumm

def insert_members_line(members, report_template, raw_header):
	#match next line after a class header's separator (=):
	SEP_RE = re.compile(r'=+\r*\n')
	header_idx = report_template.index(raw_header)
	separator = re.findall(SEP_RE, report_template[header_idx:])[0]

	#index of end of separator line
	separator_idx = report_template[header_idx:].index(separator) + len(separator) + header_idx
	result = report_template[:separator_idx] + members + report_template[separator_idx:]
	return result

def update_edition(text,end_date=datetime.now()):
	months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
	start_date = end_date + timedelta(days=-6)

	date_string = ' {0}-{1} {2} {3}\n'.format(str(start_date.day), str(end_date.day), months[end_date.month-1], str(end_date.year))
	EDITION_RE = re.compile(r'(?<=edisi).*\n', re.M|re.I)
	return EDITION_RE.sub(date_string, text)

def get_member_names(text):
	#(?<=...) : Matches if the current position in the string is preceded by a match for ... that ends at the current position
	#\s : match whitespace
	#\d : match digit
	#\w : match alphanumeric or underscore
	#https://docs.python.org/2/library/re.html
	JUZ_RE = re.compile(r'(?<=^juz\s\d\d\s).+_\w+', re.I|re.M)
	result = re.findall(JUZ_RE, text)
	return result

def get_daily_point(text, preceding_line):
	start = text.find(preceding_line)
	text = text[start:]
	opening_bracket = text.find('[')
	text = text[opening_bracket+1:]
	closing_bracket = text.find(']')
	points = map(convert, text[:closing_bracket].split('.'))
	return points

def get_name_only(name_location):
	return name_location.split('_')[0] if (name_location and '_' in name_location) else name_location

def clean_template(text):
	MEMBER_RE = re.compile(r'^.*%.*\n*', re.I|re.M)
	return MEMBER_RE.sub('', text)
