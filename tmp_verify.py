import markdownify
s = '<ul><li><p><strong>Archivo</strong></p></li></ul>'
print(markdownify.markdownify(s, heading_style='ATX'))
