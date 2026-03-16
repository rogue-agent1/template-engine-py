"""Template Engine — Jinja-like with variables, for loops, if blocks."""
import re
def render(template,context):
    def replace_var(m):
        key=m.group(1).strip(); val=context
        for part in key.split('.'):
            val=val.get(part,'') if isinstance(val,dict) else ''
        return str(val)
    def process_for(m):
        var=m.group(1); collection=m.group(2); body=m.group(3)
        items=context.get(collection,[])
        return ''.join(render(body,{**context,var:item}) for item in items)
    result=re.sub(r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}',process_for,template,flags=re.DOTALL)
    def process_if(m):
        cond=m.group(1).strip(); body=m.group(2)
        return render(body,context) if context.get(cond) else ''
    result=re.sub(r'\{%\s*if\s+(.+?)\s*%\}(.*?)\{%\s*endif\s*%\}',process_if,result,flags=re.DOTALL)
    result=re.sub(r'\{\{\s*(.+?)\s*\}\}',replace_var,result)
    return result

if __name__=="__main__":
    r=render("Hello, {{ name }}!",{'name':'Alice'})
    assert r=="Hello, Alice!"
    r2=render("{% if admin %}Admin{% endif %}",{'admin':True})
    assert r2=="Admin"
    r3=render("{% for item in items %}- {{ item }}\n{% endfor %}",{'items':['a','b','c']})
    assert '- a' in r3 and '- c' in r3
    print(f"Template: {r}, for: {r3.strip()}")
    print("All tests passed!")
