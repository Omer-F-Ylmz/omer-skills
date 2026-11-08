$kok = "C:\Projeler\omer-skills"
$model = "C:\Users\pc\Desktop\Yerel Sansursuz Model\model\Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-Q4_K_S.gguf"
$cv = "$kok\tmp\ss4\cv.gguf"

Start-Process -WindowStyle Hidden llama-server -ArgumentList "-m `"$model`" --port 8080 --jinja --reasoning-budget 0 -ngl 99 --n-cpu-moe 48 -c 4096 --control-vector-scaled `"$cv`" 1.0"
Start-Process -WindowStyle Hidden llama-server -ArgumentList "-m `"$model`" --port 8082 --jinja --reasoning-budget 0 -ngl 99 --n-cpu-moe 48 -c 4096 --control-vector-scaled `"$cv`" 2.0"
Start-Sleep 25
python "$kok\betik\vekil.py" --ust http://127.0.0.1:8080 --yedek http://127.0.0.1:8082
