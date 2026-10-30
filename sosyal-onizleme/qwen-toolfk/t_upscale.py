import time,shutil
from gradio_client import Client, handle_file
c=Client("ovi054/image-upscaler-pro")
ch=[x for x in c.config["components"] if x.get("type")=="radio"][0]["props"]["choices"]
print("choices",ch)
t=time.time()
try:
    r=c.predict(handle_file("test-tilki-kucuk.jpg"),ch[0][1] if isinstance(ch[0],list) else ch[0],api_name="/predict")
    print("OK",round(time.time()-t,1),"s",r); shutil.copy(r,"out-upscaler.webp" if str(r).endswith("webp") else "out-upscaler"+str(r)[-4:])
except Exception as e: print("ERR",type(e).__name__,str(e)[:300])
