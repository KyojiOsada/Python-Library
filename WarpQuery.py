#!/usr/bin/env python
# coding: utf-8
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

__author__	= 'Kyoji Osada at WARP-WG'
__version__	= '0.1.0'
__date__	= '2018-04-22 UTC'
__copyright__ = '2017 WARP-WG'
__license__ = 'Apache-2.0'

import re

class WarpQuery:
"""
for WARP Query Parser
"""

	operators = [';', '&', '|', '^', '==', '!=', '><', '<<', '>>', '<>', '.ij.', '.lj.', '.rj.', '.cj.', '>=', '<=', '>', '<', '?=', ':=', '.ge.', '.le.', '.gt.', '.lt.', '%3E%3E', '%3C%3C', '%3E%3C', '%3C%3E', '%3E=', '%3C=', '%3E', '%3C', '=']
	central_operators = ['==', '!=', '><', '<<', '>>', '<>', '>=', '<=', '>', '<', '?=', ':=', '=']
	compare_operators = ['==', '!=', '>=', '<=', '>', '<', '?=']
	logical_operators = ['&', '|', '^']
	join_operators = ['><', '<<', '>>', '<>']


	def __init__(self):
	"""
	constructor

	@param void
	@return void
	"""

		return


	def decode(cls, _query):
	"""
	decode Pion Query to Pion Object

	@param string Pion Query
	@return list Pion Object
	"""

		# check Empty Query String
		if _query == None:
			return []

		# form Query String for Parsing
		query_string = '&' + _query + ';'

		queries = []
		# for Proxy Parameters
		while True:

			## check Curly Brackets
			Matches = re.search('^(?:|(.*?)([&|]))({.*?[^%]})(.*)$', query_string)
			if Matches is None:
				break

			## to Readable Varliables
			all_match = Matches.group(0)
			pre_match = Matches.group(1)
			process = Matches.group(2)
			proxy = Matches.group(3)
			post_match = Matches.group(4)

			## delete Curly Bracket
			proxy = re.sub(r'^{(.*)}$', r'\1', proxy)

			## for Virtical Proxy Module
			a = proxy.find('/', 0)
			if 0 == proxy.find('/', 0):
				location = 'self'
			## for Horizontal Proxy Module
			else:
				Matches = re.search(r'^(http(?:|s)://.+?)/', proxy)
				if Matches != None:
					location = Matches.group(1)
					proxy = proxy.replace(location, '')
				## for Others
				else:
					raise SyntaxError('The Proxy Parameters are having unknown URL scheme: ' + proxy)

			### to Objects
			queries.append([
				process,
				location,
				'{}',
				proxy,
			])

			## reform Query String for Parsing
			query_string = pre_match + post_match

		# escape Operators
		esc_operators = []
		for i, operator in enumerate(cls.operators):
			esc_operators.append(re.escape(operator))

		# form Operators Regex
		operators_regex = '^(.*?)(' + '|'.join(esc_operators) + ')(.*?)$'

		# Query to Parts
		query_parts = []
		while True:
			## matching Operators
			Matches = re.search(operators_regex, query_string)
			if Matches is None:
				break

			## to Readable Varliables
			all_match = Matches.group(0)
			operand = Matches.group(1)
			operator = Matches.group(2)
			post_match = Matches.group(3)

			## from Alias Operators to Master Operators
			if operator == '.ge.' or operator == '%3E=':
				operator = '>='
			elif operator == '.le.' or operator == '%3C==':
				operator = '<='
			elif operator == '.gt.' or operator == '%3E':
				operator = '>'
			elif operator == '.lt.' or operator == '%3C':
				operator = '<'
			elif operator == '.ij.' or operator == '%3E%3C':
				operator = '><'
			elif operator == '.lj.' or operator == '%3C%3C':
				operator = '<<'
			elif operator == '.rj.' or operator == '%3E%3E':
				operator = '>>'
			elif operator == '.cj.' or operator == '%3C%3E':
				operator = '<>'

			## map to Query Parts
			if operand != '':
				query_parts.append(operand)

			query_parts.append(operator)

			## from Post Matcher to Query String
			query_string = post_match

		# check Data-Type-Head Module
		data_type = False
		if 'data-type' in query_parts:
			data_type_id = query_parts.index('data-type')

			if query_parts[data_type_id + 1] == ':=':
				data_type = query_parts[data_type_id + 2]

		# map to Queries
		for i, query_part in enumerate(query_parts):

			## not Central Operators
			if query_part not in cls.central_operators:
				continue

			## to Readable Varliables
			logical_operator = query_parts[i - 2];
			left_operand = query_parts[i - 1];
			central_operator = query_part;
			right_operand = query_parts[i + 1];

			## for Data-Type-Head Module
			### for Strict Data Type
			if data_type == 'true':
				regex = '^%(?:22|27|["\'])(.*?)%(?:22|27|["\'])$';
				### delete first and last quotes for String Data Type
				if re.search(regex, right_operand):
					right_operand = re.sub(regex, r'\1', right_operand)
				### for Not String Type
				else:
					#### to Boolean
					if right_operand == 'true':
						right_operand = True
					#### to Boolean
					elif right_operand == 'false':
						right_operand = False
					#### to Null
					elif right_operand == 'null':
						right_operand = None
					#### to Integer
					elif re.search('^\d\z|\A[1-9]\d+$', right_operand):
						right_operand = int(right_operand)
					#### to Float
					elif re.search('^\d\.\d+\z|\A[1-9]\d+\.\d+$', right_operand):
						right_operand = float(right_operand)

			## validate Left Operand
			if left_operand in cls.operators:
				raise SyntaxError('The parameter is having invalid left operands: ' + _query)

			## validate Right Operand
			### to Empty String
			if right_operand in cls.logical_operators or right_operand == ';':
				right_operand = '';
			### for Double NV Operators
			elif right_operand in cls.central_operators:
				raise SyntaxError('The parameter is having double comparing operators: ' + _query)

			## map to Queries
				### for Head Parameters
			if central_operator == ':=':
				#### validate Logical Part
				if logical_operator != '&':
					raise SyntaxError('The Head Parameters must be a “and” logical operator: ' + _query)

			### for Assign Parameters
			elif central_operator == '=':
				#### validate Logical Part
				if logical_operator != '&':
					raise SyntaxError('The Assign Parameters must be a “&” logical operator: ' + _query)

			### for Join Parameters
			elif central_operator in cls.join_operators:
				#### validate Logical Part
				if logical_operator != '&':
					raise SyntaxError('The Join Parameters must be a “&” logical operator: ' + _query)

			### for Search Parameters
			elif central_operator in cls.compare_operators:
				#### validate Logical Part
				if logical_operator not in cls.logical_operators:
					raise SyntaxError('The Search Parameters are having invalid logical operators: ' + _query)

			### Others
			else:
				continue

			### to Queries
			queries.append([
				logical_operator,
				left_operand,
				central_operator,
				right_operand,
			])

		# init Searches 1st Logical Operator
		queries[0][0] = ''

		# return
		return queries;


	def encode(cls, _object = None):
	"""
	encode Pion Object to Pion Query

	@param list Pion Object
	@return string Pion Query
	"""

		# check Empty Object
		if _object == None:
			return ''

		# drop First Logical Operator
		if queries[0][0] != '':
			queries[0][0] = ''

		# check Data Type Flag
		data_type_flag = False
		for i, lists in enumerate(_object):
			for j, value in enumerate(lists):
				## for Not Data Type
				if value != 'data-type':
					continue

				## for Data Type
				# Notice: Processing must be not breaked because there ware multiple the value of “data-type”.
				if _object[i][j + 2] == True:
					data_type_flag = True;

		# to Query String
		query_string = '';
		for i, lists in enumerate(_object):

			print lists
			if lists[2] == '{}':
				lists[1] = '' if lists[1] == 'self' else lists[1]
				lists[1] = '{' + lists[1]
				lists[2] = ''
				lists[3] = lists[3] + '}'

			for j, value in enumerate(lists):
				## for Stric Data Type
				if data_type_flag:
					### for Value of Strint Type
					if j == 3:
						if is_string(value):
							value = "'" + value + "'"

				## for Value of Boolean and Null Type
				if j == 3:
					if value == True:
						value = 'true'
					elif value == False:
						value = 'false'
					elif value == None:
						value = 'null'

				### to Query String
				query_string += value

		# return
		return query_string
