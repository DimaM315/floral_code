
class KeyWords:
	operations_reg_exp = r"\s(\*\*|//|\+=|!=|==|-=|<=|>=|-|=|\*|\+|/|<|>|&|:=|%)\s"

	comment_reg_exp = r"\#\s?(.*)"

	primary_values_reg_exp = r"(True|False|None)"

	python_method_reg_exp = r"(print|len|range|bin|count|replace|warning|[\s|\(]int|str|list|open|any|isinstance)\("
	obj_method_reg_exp = r"\.(.+)\("

	key_word_reg_exp = r"(import|while|with|from|return|assert|elif|else|raise|for\s|if\s|pass|break|continue|\sas\s|\sin\s|\sand\s|\sor\s|not\s)"


	#string_reg_exp = r"[^\\](\".*?[^\\]\")|(\'.*?\')"
	string_reg_exp = r"(\".*?\")|(\'.*?\')"


	# если число будет в строке например: t = " 55 ". Это регулярное выр. заметчит его.
	int_reg_exp = r"([\s|\(|\[|\{])(\d+\.?\d*)"



class HtmlEntities:
	paragraf_tab = "<p style='margin-left:{0}px;'>"


	# for paint_def_method()
	span_def = "<span class='code-def-keyword'>{0}</span> "
	span_method_def = " <span class='code-method-def'>{0}</span>"
	span_method_param = "<span class='code-method-param'>{0}</span>"

	span_int = "{0}<span class='code-int'>{1}</span>"
	span_string = "<span class='code-str'>{0}</span>"
	span_key_word = "<span class='code-keyword'>{0}</span>"
	span_operation = " <span class='code-operation'>{0}</span> "
	span_comment = "<span class='code-comment'>{0}</span>"
	span_primary_values = "<span class='code-primary-value'>{0}</span>"

	# for paint_python_method() - len, bin, "count", "replace", ...
	span_method = "<span class='code-method'>{0}</span>("

	
	
	
