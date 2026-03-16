    #!/usr/bin/env python3
    """Template engine — variables, loops, conditionals, filters."""
    import re, sys

    class Template:
        def __init__(self,text): self.text=text; self.filters={"upper":str.upper,"lower":str.lower,"title":str.title,"len":len,"reverse":lambda s:s[::-1]}
        def render(self,context):
            result=self.text
            # Loops: {% for item in list %}...{% endfor %}
            def replace_for(m):
                var,iterable,body=m.group(1),m.group(2),m.group(3)
                items=self._resolve(iterable,context)
                if not items: return ""
                parts=[]
                for item in items:
                    ctx={**context,var:item}
                    parts.append(Template(body).render(ctx))
                return "".join(parts)
            result=re.sub(r'{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}(.*?){%\s*endfor\s*%}',replace_for,result,flags=re.DOTALL)
            # Conditionals: {% if var %}...{% else %}...{% endif %}
            def replace_if(m):
                cond,true_part=m.group(1),m.group(2)
                false_part=m.group(4) if m.group(3) else ""
                return true_part if self._resolve(cond,context) else false_part
            result=re.sub(r'{%\s*if\s+(\w+)\s*%}(.*?)({%\s*else\s*%}(.*?)){0,1}{%\s*endif\s*%}',replace_if,result,flags=re.DOTALL)
            # Variables with filters: {{ var|filter }}
            def replace_var(m):
                expr=m.group(1).strip(); parts=expr.split("|")
                val=self._resolve(parts[0].strip(),context)
                for f in parts[1:]:
                    f=f.strip()
                    if f in self.filters: val=self.filters[f](val)
                return str(val) if val is not None else ""
            result=re.sub(r'{{\s*(.+?)\s*}}',replace_var,result)
            return result
        def _resolve(self,key,context):
            parts=key.split(".")
            val=context
            for p in parts: val=val.get(p) if isinstance(val,dict) else getattr(val,p,None)
            return val

    if __name__ == "__main__":
        tmpl=Template("""Hello {{ name|upper }}!
{% if admin %}You are an admin.{% else %}You are a user.{% endif %}
Your items:
{% for item in items %}- {{ item }}
{% endfor %}""")
        print(tmpl.render({"name":"rogue","admin":True,"items":["python","crypto","systems"]}))
