import re


from mixin import KeyWords, HtmlEntities


class FloralCode(KeyWords, HtmlEntities):
	"""
		Class do paint. Work with only code are respective PEP8 stnd.
		Create tab-space with <p>-tags.
		painting key word("import", "for", "if", "+", ">=") with <span>-tags
	"""


	def __init__(self, text=None, file_path=False):
		self.file_path = file_path

		if text:
			self.text = text
		elif file_path:
			self.text = self.extracting_text(file_path)
	

	def text_paint(self):
		"""
		main function. Make control for paint process.
		"""
		lines = self.text.split('\n')

		for i, line in enumerate(lines):
			line = self.text_spanification(line)
			line = self.text_paragrafication(line)
			lines[i] = line

		self.text = '\n'.join(lines)



	def text_spanification(self, text_line):
		if re.search(r"[\s|\t]*def\s|class\s", text_line):
			text_line = self.paint_def_method(text_line)
			return text_line

		if "#" in text_line:
			text_line = self.line_with_comment_handler(text_line)
			return text_line

		text_line = self.paint_string(text_line)
		
		text_line = self.paint_operation(text_line)
		text_line = self.paint_primary_values(text_line)
		text_line = self.paint_python_method(text_line)
		text_line = self.paint_key_words(text_line)
		text_line = self.paint_int(text_line)

		return text_line


	def text_paragrafication(self, text_line):
		one_tab_in_px = 50
		p = self.paragraf_tab.format(text_line.count("\t") * one_tab_in_px)

		return p + text_line.replace("\t", "") + "</p>"


	# methods paintor
	def paint_def_method(self, text_line):
		assert "def" in text_line or "class" in text_line
		text_line = re.sub(
				r" ([A-z0-9]*)", 
				self.span_method_def.format(r"\1"), text_line,
				1) # only first mantch, because will subrtact in brackets
		
		try:
			# in case: "class Name:"(without brackets) will called AttrError
			text_in_brackets = re.search(r"\((.*)\)", text_line).groups()[0]
		except AttributeError as e:
			text_in_brackets = ""
		
		text_in_brackets = self.method_param_handler(text_in_brackets)
		text_line = re.sub(r"\((.*)\)", "("+text_in_brackets+")", text_line)
		
		text_line = text_line.replace("def ", self.span_def.format("def"))
		text_line = text_line.replace("class ", self.span_def.format("class"))

		return text_line


	def paint_int(self, text_line):
		# painting anything int in code, except for the int in the names or str(\"\")
		
		# in case, when int into the string. Exp: t = "55"
		if "class='code-str'" in text_line:
			# There text_line have span-str
			return self.paint_with_escape_str(text_line, self.span_int, self.int_reg_exp)

		return re.sub(self.int_reg_exp, self.span_int.format(r"\1", r"\2"), text_line)


	def paint_string(self, text_line):
		# painting anything match "some text...". Exp: t = "". Res: t = <span>""</span> 
		return re.sub(self.string_reg_exp, self.span_string.format(r"\1\2"), text_line)	


	def paint_key_words(self, text_line):
		# import, while, with, from, return, assert, elif, else as, in, and ...
		return re.sub(self.key_word_reg_exp, self.span_key_word.format(r"\1")+" ", text_line)


	def paint_python_method(self, text_line):
		# "print", "len", " range", "bin", "count", "replace", "warning", "int", "str"
		text_line = re.sub(self.python_method_reg_exp, self.span_method.format(r"\1"), text_line)
		text_line = re.sub(self.obj_method_reg_exp, "." + self.span_method.format(r"\1"), text_line)
		return text_line


	def paint_primary_values(self, text_line):
		# True, False, None

		# in case, when primary value into the string. Exp: t = "True"
		if "class='code-str'" in text_line:
			# There text_line have span-str
			return self.paint_with_escape_str(text_line, 
								self.span_primary_values, 
								self.primary_values_reg_exp)

		return re.sub(self.primary_values_reg_exp, self.span_primary_values.format(r"\1"), text_line)


	def paint_operation(self, text_line):
		# = + - == > < <= >= ** *
		if "class='code-str'" in text_line:
			# There text_line have span-str
			return self.paint_with_escape_str(text_line, self.span_operation, self.operations_reg_exp)

		return re.sub(self.operations_reg_exp, self.span_operation.format(r"\1"), text_line)


	def paint_comment(self, text_line):
		#  \# text before...
		if "class='code-str'" in text_line:
			# There text_line have span-str
			return self.paint_with_escape_str(text_line, self.span_comment, self.comment_reg_exp)

		return re.sub(self.comment_reg_exp, self.span_comment.format(r"# \1"), text_line)


	# support methods
	def paint_with_escape_str(self, text_line, span, reg_exp):
		line_bits = text_line.split("code-str")
		for i, bit in enumerate(line_bits):
			if i == 0:
				# There is no str
				line_bits[i] = re.sub(
					reg_exp, 
					span.format(r"\1", r"\2"), 
					line_bits[i])	
			elif i != 0:
				# There is str under first </span>
				bit_bits = bit.split('</span>', 1)
				line_bits[i] = '</span>'.join((bit_bits[0], re.sub(
									reg_exp, 
									span.format(r"\1", r"\2"), 
									bit_bits[1])))
		return "code-str".join(line_bits)


	def method_param_handler(self, text_in_brackets):
		# hendle text in def-function brackers, paint parametrs
		assert isinstance(text_in_brackets, str)
		assert "(" not in text_in_brackets and ")" not in text_in_brackets

		if text_in_brackets == "":
			return ""

		span_params = "<span class='code-method-param'>{0}</span>"

		list_params_in_brackets = text_in_brackets.split(', ')
		
		for i, param in enumerate(list_params_in_brackets):
			if "=" not in param:	
				list_params_in_brackets[i] = span_params.format(param)
				continue
		
			param_bits = param.split("=")	
			param_bits[0] = span_params.format(param_bits[0]) # Поз 0: argument name
			
			# Поз 1: argument value. Define arg type
			if re.search(r"\d*", param_bits[1]).group() == param_bits[1] \
							or param_bits[1] in ("True", "False", "None"):
				param_bits[1] = "<span class='code-int'>"+param_bits[1]+"</span>"
			elif "\"" == param_bits[1][0] and "\"" == param_bits[1][-1]:
				param_bits[1] = "<span class='code-str'>"+param_bits[1]+"</span>"

			list_params_in_brackets[i] = "<span class='code-operation'>=</span>".join(param_bits)


		return ', '.join(list_params_in_brackets)


	def line_with_comment_handler(self, text_line):
		line_bits = text_line.split("#", 1) # line_bits[0] - common code, line_bits[1] - commented text
		
		line_bits[0] = self.text_spanification(line_bits[0])
		line_bits[1] = self.paint_comment("#" + line_bits[1])

		return line_bits[0] + line_bits[1]


	# file handler methods
	def extracting_text(self, file_path, mode='r+'):
		with open(file_path, mode, encoding="utf-8") as f:
			return f.read()


	def save_text(self, mode='w'):
		with open(self.file_path, mode, encoding="utf-8") as f:
			f.write(self.text)



