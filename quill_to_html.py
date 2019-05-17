from cgi import escape

QUILL_REPLACE_INLINE = [{'quill':'script', 'value': 'super', 'htmls':'<sup{}>', 'htmle':'</sup>'},
{'quill':'script', 'value': 'sub', 'htmls':'<sub{}>', 'htmle':'</sub>'},
{'quill':'bold', 'value': True, 'htmls':'<strong{}>', 'htmle':'</strong>'},
{'quill':'italic', 'value': True, 'htmls':'<em{}>', 'htmle':'</em>'},
{'quill':'strike', 'value': True, 'htmls':'<s{}>', 'htmle':'</s>'},
{'quill':'underline', 'value': True, 'htmls':'<u{}>', 'htmle':'</u>'},
]
QUILL_STYLE_INLINE = [{'quill':'color', 'style':'color:', 'value': True},
{'quill':'background', 'style':'background-color:', 'value': True},
]
QUILL_CLASSES = [{'quill':'size', 'value': True, 'class_base':'ql-size-',},
{'quill':'font', 'value': True, 'class_base':'ql-font-',},
{'quill':'align', 'value': True, 'class_base':'ql-align-',},
{'quill':'indent', 'value': True, 'class_base':'ql-indent-',},
{'quill':'direction', 'value': True, 'class_base':'ql-direction-',},
]

true = True

def quill_delta_to_html(quill_dict):
    if 'ops' in quill_dict:
        line_attributes = {}
        result = ''
        end_of_lane_tags = ''
        for operation in quill_dict['ops']:
            if 'attributes' in operation:
                attributes = operation['attributes']
            else:
                attributes = {}

            if 'insert' in operation:
                text = operation['insert']
                if text == '\n':
                    line_attributes, start_tags, end_of_lane_tags = parse_line_attributes(attributes, old_attributes = line_attributes)
                    result += start_tags
                else:
                    text_to_add = parse_text_attributes(text, attributes)
                    result += text_to_add + end_of_lane_tags
        for i in range(len(QUILL_REPLACE_INLINE)):
            repl = QUILL_REPLACE_INLINE[i]
            result = result.replace(repl['htmle'] + repl['htmls'], '')
        return result


def parse_line_attributes(attributes, old_attributes={}):
    text_beginning_of_lane = ''
    text_ending_of_lane = ''
    text_start_block = ''
    text_end_block = ''
    if 'list' in attributes and 'list' in old_attributes:
        if attributes['list'] != old_attributes['list']:
            if attributes['list'] == 'ordered':
                text_start_block += '<ol>'
            else:
                text_start_block += '<ul>'
            if old_attributes['list'] == 'ordered':
                text_end_block += '</ol>'
            else:
                text_end_block += '</ul>'
        if 'indent' in attributes:
            text_beginning_of_lane += '<li class=\'ql-indent-'+ str(attributes['indent']) +'\'>'
        else:
            text_beginning_of_lane += '<li>'
        text_ending_of_lane += '</li>'
    elif 'list' in attributes:
        if attributes['list'] == 'ordered':
            text_start_block += '<ol>'
        else:
            text_start_block += '<ul>'
        if 'indent' in attributes:
            text_beginning_of_lane += '<li class=\'ql-indent-'+ str(attributes['indent']) +'\'>'
        else:
            text_beginning_of_lane += '<li>'
        text_ending_of_lane += '</li>'
    elif 'list' in old_attributes:
        if old_attributes['list'] == 'ordered':
            text_end_block += '</ol>'
        else:
            text_end_block += '</ul>'
    
    return attributes, text_end_block + text_start_block + text_beginning_of_lane, text_ending_of_lane


def parse_text_attributes(text, attributes, old_attributes={}):
    result = text
    classes = ''
    styles = ''
    begin = ''
    end = ''
    for i in range(len(QUILL_CLASSES)):
        repl = QUILL_CLASSES[i]
        if repl['quill'] in attributes:
            if repl['value']:
                if classes == '':
                    classes = repl['class_base'] + attributes[repl['quill']]
                else:
                    classes += ' ' + repl['class_base'] + attributes[repl['quill']]
            else:
                if classes == '':
                    classes = repl['class_base']
                else:
                    classes += ' ' + repl['class_base']
    
    for i in range(len(QUILL_STYLE_INLINE)):
        repl = QUILL_STYLE_INLINE[i]
        if repl['quill'] in attributes:
            if repl['value']:
                if styles == '':
                    styles = repl['style'] + ':' + attributes[repl['quill']]
                else:
                    styles += ' ' + repl['style'] + ':' + attributes[repl['quill']]
            else:
                if styles == '':
                    styles = repl['class_base']
                else:
                    styles += ' ' + repl['class_base']
    
    attribs = ''
    if styles != '' and classes != '':
        attribs = ' style=\'' + styles + '\' class=\'' + classes + '\' '
    elif styles != '':
        attribs = ' style=\'' + styles + '\' '
    elif styles != '' and classes != '':
        attribs = ' class=\'' + classes + '\' '

    for i in range(len(QUILL_REPLACE_INLINE)):
        repl = QUILL_REPLACE_INLINE[i]
        if repl['quill'] in attributes and attributes[repl['quill']] == repl['value']:
            result = repl['htmls']+result+repl['htmle']
    if 'link' in attributes and attributes['link']!='':
        result = '<a href="' + attributes['link'] + '" target="_blank">' + result + '</a>'
    return begin + result + end