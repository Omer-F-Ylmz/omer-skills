import shutil,os
d=os.path.join(os.environ['LOCALAPPDATA'],'Temp','.playwright-mcp');os.makedirs(d,exist_ok=True)
print(shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pw-ac.js'),d))
