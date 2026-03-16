import re
def render(template,context):
    def replace_var(m):
        key=m.group(1).strip()
        val=context
        for part in key.split('.'): val=val.get(part,'') if isinstance(val,dict) else getattr(val,part,'')
        return str(val)
    result=re.sub(r'\{\{\s*(.+?)\s*\}\}',replace_var,template)
    def process_for(m):
        var=m.group(1); collection=m.group(2); body=m.group(3)
        items=context.get(collection,[])
        return ''.join(render(body,{**context,var:item}) for item in items)
    result=re.sub(r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}',process_for,result,flags=re.DOTALL)
    def process_if(m):
        cond=m.group(1).strip(); body=m.group(2)
        val=context.get(cond)
        return render(body,context) if val else ''
    result=re.sub(r'\{%\s*if\s+(.+?)\s*%\}(.*?)\{%\s*endif\s*%\}',process_if,result,flags=re.DOTALL)
    return result
if __name__=="__main__":
    tmpl="Hello, {{ name }}! You have {{ count }} messages."
    r=render(tmpl,{'name':'Alice','count':5})
    assert r=="Hello, Alice! You have 5 messages."
    tmpl2="{% if admin %}Admin{% endif %}"
    assert render(tmpl2,{'admin':True})=="Admin"
    assert render(tmpl2,{'admin':False})==""
    tmpl3="{% for item in items %}- {{ item }}\n{% endfor %}"
    r3=render(tmpl3,{'items':['a','b','c']})
    assert '- a' in r3 and '- c' in r3
    print(f"Template: {r}")
    print("All tests passed!")
