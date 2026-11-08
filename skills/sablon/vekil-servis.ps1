# Yerel model + vekil servisi. Once 8080 (dusuk olcek), sonra 8082 (yuksek olcek), en son vekil.
$kok = "C:\Projeler\omer-skills"
$model = "C:\Users\pc\Desktop\Yerel Sansursuz Model\model\Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-Q4_K_S.gguf"
$cv = "$kok\tmp\ss4\cv.gguf"

Start-Process -WindowStyle Hidden llama-server -ArgumentList "-m `"$model`" --port 8080 --jinja --ctx-size 32768 -ngl 99 --control-vector-scaled `"$cv`" 1.0"
Start-Process -WindowStyle Hidden llama-server -ArgumentList "-m `"$model`" --port 8082 --jinja --ctx-size 32768 -ngl 99 --control-vector-scaled `"$cv`" 2.0"
Start-Sleep 20
python "$kok\betik\vekil.py" --ust http://127.0.0.1:8080 --yedek http://127.0.0.1:8082
