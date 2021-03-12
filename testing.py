import unittest
import re

from floral_code import FloralCode


class Test(unittest.TestCase):
	def setUp(self):
		self.paintor = FloralCode('some_file.docx')
	

	def test_def_method_case(self):
		# simple
		self.assertEqual(self.paintor.paint_def_method("def some_func(s):"),
					 "<span class='code-def-keyword'>def</span> <span class='code-method-def'>some_func</span>(<span class='code-method-param'>s</span>):")
		self.assertEqual(self.paintor.paint_def_method("class SomeCls:"),
					 "<span class='code-def-keyword'>class</span> <span class='code-method-def'>SomeCls</span>:")
		# without "def/class" - word
		with self.assertRaises(AssertionError):
				self.paintor.paint_def_method("t = 'hello'")
		# hard case
		self.assertEqual(self.paintor.paint_def_method("def some_func(s, s1, s2=\"some\"):"),
					 "<span class='code-def-keyword'>def</span> <span class='code-method-def'>some_func</span>(<span class='code-method-param'>s</span>, <span class='code-method-param'>s1</span>, <span class='code-method-param'>s2</span><span class='code-operation'>=</span><span class='code-str'>\"some\"</span>):")


	def test_int_case(self):
		# simple 
		self.assertEqual(self.paintor.paint_int(
			"t = 500"), 
			"t = <span class='code-int'>500</span>")
		# without int
		self.assertEqual(self.paintor.paint_key_words(
			"t = 'hello'"),
			"t = 'hello'")
		# hard case
		self.assertEqual(self.paintor.paint_int(
			"t = 500; x = <span class='code-str'>' 500 '</span> * 0.5"), 
			"t = <span class='code-int'>500</span>; x = <span class='code-str'>' 500 '</span> * <span class='code-int'>0.5</span>")


	def test_key_word_case(self):
		# simple 
		self.assertEqual(self.paintor.paint_key_words(
			"from re import *"), 
			"<span class='code-keyword'>from</span>  re <span class='code-keyword'>import</span>  *")
		# without key words
		self.assertEqual(self.paintor.paint_key_words(
			"t = 'hello'"),
			"t = 'hello'")
		# hard case
		self.assertEqual(self.paintor.paint_key_words(
			"with open('ge.txt' if not 5==5 else 'ge2.txt')"),
			"<span class='code-keyword'>with</span>  open('ge.txt' <span class='code-keyword'>if </span> <span class='code-keyword'>not </span> 5==5 <span class='code-keyword'>else</span>  'ge2.txt')") 


	def test_primary_value_case(self):
		self.assertEqual(self.paintor.paint_primary_values(
			"a = True"),
			"a = <span class='code-primary-value'>True</span>" )
		# without primary values
		self.assertEqual(self.paintor.paint_primary_values(
			"t = 'hello'"),
			"t = 'hello'")
		# hard case
		self.assertEqual(self.paintor.paint_primary_values(
			"t = None; x1 = <span class='code-str'>'True'</span>"),
			"t = <span class='code-primary-value'>None</span>; x1 = <span class='code-str'>'True'</span>")


	def test_operation_case(self):
		self.assertEqual(self.paintor.paint_operation(
			"if 2 + 2 == 4 ** 4:"),
			"if 2 <span class='code-operation'>+</span> 2 <span class='code-operation'>==</span> 4 <span class='code-operation'>**</span> 4:")
		# without operation
		self.assertEqual(self.paintor.paint_operation(
			"import re"),
			"import re")


	def test_comment_case(self):
		self.assertEqual(self.paintor.paint_comment(
				"# first comment"), 
				"<span class='code-comment'># first comment</span>")
		# without comment
		self.assertEqual(self.paintor.paint_comment(
			"t = 'hello'"),
			"t = 'hello'")
		# hard case
		self.assertEqual(self.paintor.paint_comment(
				"# first comment#2"), 
				"<span class='code-comment'># first comment#2</span>")
		self.assertEqual(self.paintor.paint_comment(
				"gge = <span class='code-str'>\"fake # comment\"</span>"), 
				"gge = <span class='code-str'>\"fake # comment\"</span>")


	def test_string_case(self):
		# simple 
		self.assertEqual(self.paintor.paint_string(
			't = "Hello world"; t2 = "bay"'),
			"t = <span class='code-str'>\"Hello world\"</span>; t2 = <span class='code-str'>\"bay\"</span>")
		self.assertEqual(self.paintor.paint_string(
				"t = 'hello'"), 
				"t = <span class='code-str'>'hello'</span>")
		# without string
		self.assertEqual(self.paintor.paint_string(
			"t = 6"),
			"t = 6")
		# hard case
		self.assertEqual(self.paintor.paint_string(
			"t = 'i am \"super\" str'; x = len('long\"str')"),
			"t = <span class='code-str'>'i am \"super\" str'</span>; x = len(<span class='code-str'>'long\"str'</span>)")


	def test_tabulation(self):
		# text_paragrafication - method make tabs with a <p margin="-px"> tags
		self.assertEqual(self.paintor.text_paragrafication(""), "<p style='margin-left:0px;'></p>")
		self.assertEqual(self.paintor.text_paragrafication("\t"), "<p style='margin-left:50px;'></p>")
		self.assertEqual(self.paintor.text_paragrafication("	"), "<p style='margin-left:50px;'></p>")
		self.assertEqual(self.paintor.text_paragrafication("	\t"), "<p style='margin-left:100px;'></p>")
		self.assertEqual(self.paintor.text_paragrafication("\t\t"), "<p style='margin-left:100px;'></p>")

		self.assertEqual(
			self.paintor.text_paragrafication("\t\t\t"), "<p style='margin-left:150px;'></p>")
		self.assertEqual(
			self.paintor.text_paragrafication("			"), "<p style='margin-left:150px;'></p>")




if __name__ == '__main__':
	unittest.main()

