#!/usr/bin/env python3
"""Template engine — {{ var }}, {% for %}, {% if %} syntax."""
import re
def render(template,context):
    result=template
    # Handle for loops
    for_pattern=r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
    while re.search(for_pattern,result,re.DOTALL):
        m=re.search(for_pattern,result,re.DOTALL)
        var,collection,body=m.group(1),m.group(2),m.group(3)
        items=context.get(collection,[])
        expanded="".join(render(body,{**context,var:item}) for item in items)
        result=result[:m.start()]+expanded+result[m.end():]
    # Handle if
    if_pattern=r'\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}'
    while re.search(if_pattern,result,re.DOTALL):
        m=re.search(if_pattern,result,re.DOTALL)
        cond,body=m.group(1),m.group(2)
        expanded=body if context.get(cond) else ""
        result=result[:m.start()]+expanded+result[m.end():]
    # Handle variables
    result=re.sub(r'\{\{\s*(\w+)\s*\}\}',lambda m:str(context.get(m.group(1),"")),result)
    return result
def main():
    tpl="Hello {{ name }}! {% for item in items %}* {{ item }}\n{% endfor %}"
    print(render(tpl,{"name":"World","items":["a","b","c"]}))
if __name__=="__main__":main()
