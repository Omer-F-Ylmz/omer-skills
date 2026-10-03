# TOKEN-6f — Headroom sıcak önbellek kırılması

## K1 Mühür (dalga başı)

- settings d624c65bfad79cee · hooks f226ffce582b5bdc · mcpServers 50d989fb836cac49 (üst + proje) · mcp 19 · plugin 47/53 · skill 2068. settings ve hooks sha8'i TOKEN-6c-R ile aynı.
- Çalışan proxy: pid 39584, `%LOCALAPPDATA%\Headroom\headroom\runtime\python\python.exe`, bayraklar `--port 6768 --no-http --no-rate-limit --log-messages`. Sürüm **headroom-ai 0.39.0**. Ayrıca uv tool olarak 0.37.0 kurulu; bu yalnız CLI, trafik ona gitmiyor.
- Yamalanacak dosyalar (runtime venv, site-packages): `headroom/proxy/handlers/anthropic.py` a01ca8042ad8f293 · `headroom/cache/prefix_tracker.py` 6ffca9b3da0a6a58 · `headroom/transforms/cold_prefix.py` 0a02799830e77857.
- Mod: `--mode` bayrağı yok, `HEADROOM_MODE` de tanımsız. Bu yüzden varsayılan **cache** geçerli (`cli/proxy.py:1266`).
- OUTPUT_SHAPER: User ortam değişkeni olarak tanımlı (boolean kontrolü; değer basılmadı). /health runtime_env sha8 391552c0.
- OUTPUT_HOLDOUT: User/Machine/Process ortamında tanımsız. /health'te değeri var (f875a380), yani bellek içi runtime-env override'ı (`proxy/runtime_env.py:83` `_overrides`, `:108` `set_overrides`, `POST /admin/runtime-env`); dosyası yok. Kaynak koddaki varsayılan `"0"`: `proxy/handlers/anthropic.py:3371`.
- VERBOSITY_LEVEL: HOLDOUT ile aynı durumda, runtime-env override'ı (cc11310c). Varsayılan `DEFAULT_VERBOSITY_LEVEL = 2`: `proxy/output_shaper.py:92`, okunduğu yer `:126`.
- Headroom kendi testlerini paketle dağıtmıyor: site-packages altında `tests`/`test*` dizini 0.
