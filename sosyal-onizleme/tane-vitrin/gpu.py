import subprocess
print(subprocess.run(['nvidia-smi','--query-gpu=utilization.gpu,memory.used,memory.total','--format=csv'],capture_output=True,text=True).stdout)
print(subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv'],capture_output=True,text=True).stdout)
