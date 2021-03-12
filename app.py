import re
from floral_code import FloralCode


def render_template(body, template_path="some_page.html", update=False):
	"""
	Simplest renderer for convenient watching.
	:body. That will insert into html-tag body. And will be wrapped to div tag, with class .block_code.
	"""
	assert isinstance(body, str)

	with open(template_path, "r+", encoding="utf-8") as f:
		template_text = f.read()

	if update:
		templ_parts = template_text.split("div")
		template_text = templ_parts[0] + "div class='block_code'>" + body + "</div" + templ_parts[2]
	elif "<div class=\"block_code\"></div>" in template_text:
		template_text = template_text.replace(
						"<div class=\"block_code\"></div>", 
						"<div class=\"block_code\">"+body+"</div>"
					)
	else:
		print("Body was not added!")
		return False

	with open(template_path, "w", encoding="utf-8") as f:
		f.write(template_text)
	print("Body added successfully!")



FILE = 'some_code.txt'


if __name__ == '__main__':
	painter = FloralCode(file_path=FILE)
	painter.text_paint()
	render_template(painter.text, update=True)

