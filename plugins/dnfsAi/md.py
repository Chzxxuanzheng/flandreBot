from nonebot.adapters.onebot.v11 import MessageSegment
from re import compile, MULTILINE
from pillowmd import LoadMarkdownStyles
from util.md import md2pic

qqTable = LoadMarkdownStyles('mdStyle/qq-table')

async def betterMd(md: str) -> list[MessageSegment]:
	# 匹配 Markdown 表格（以 | 开头，至少两行，允许前后有空行）
	table_pattern = compile(
		r'((?:^\s*\|.*\|\s*$\n)+^\s*\|(?:\s*-+\s*\|)+\s*$\n(?:^\s*\|.*\|\s*$\n?)+)',
		MULTILINE
	)

	# 用正则 split 并标注
	parts = []
	last_end = 0
	for m in table_pattern.finditer(md):
		# 非表格部分
		if m.start() > last_end:
			parts.append({'type': 'text', 'content': md[last_end:m.start()]})
		# 表格部分
		parts.append({'type': 'table', 'content': m.group(0)})
		last_end = m.end()
	# 结尾剩余部分
	if last_end < len(md):
		parts.append({'type': 'text', 'content': md[last_end:]})

	out = []
	for part in parts:
		if part['type'] == 'text':
			out.append(MessageSegment.text(part['content'].strip()+'\n'))
		elif part['type'] == 'table':
			# 处理表格内容，假设表格内容是纯文本
			out.append(await md2pic(part['content'], qqTable))
	return out