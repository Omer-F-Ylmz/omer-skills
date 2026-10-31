# NVDA

- tür: varlik · durum: KAYITSIZ · videolar: Dd0ZDPRjIWA,Dd48nVoD7FR,DdeFYOXH6XY,DdzGPvzIN4C,De7CBz-q42H,DeHhu6qlL7Q,DeOPnJDltkN,DeOQHqBk9Pz,DePWmOHCPX1,DeaQMKLgeT5,Deet0VsP-KQ,DegQTLBEzu6,Dejzt54pZ0A,Der12cMk0_N,Det0-D8Oc41
- bizde: yok

## Özellikler
- TradingAgents çerçevesi NVDA için karar üretiyor: propagate('NVDA', '2026-09-01') bir karar döndürüyor
- Yapılandırmada deep_think_llm ve quick_think_llm ile iki ayrı model seçilebiliyor (model adları alıntıda bozuk)
- max_debate_rounds ayarı var (örnekte 2)
- Desteklenen sağlayıcılar: openai, google, anthropic, xai, deepseek, groq, ollama, openai_compatible (metin kısmen bozuk)
- Filings panelinde NVDA için 8-K kaydı var (29 Nis 2024, yeni ürün/iş)

## Videoda yapılış
from tradingagents.graph.trading_graph import TradingAgentsGraph; from tradingagents.default_config import DEFAULT_CONFIG; config = DEFAULT_CONFIG.copy(); config['max_debate_rounds'] = 2; ta = TradingAgentsGraph(debug=True, config=config); decision = ta.propagate('NVDA', '2026-09-01'); print(decision). Alternatif olarak main.py çalıştırılır. Ayrıntılı seçenekler tradingagents/default_config.py dosyasında.

## Bizdeki karşılık ve fark
yok

## Al
Tek fonksiyonla (propagate) ticker ve tarih için karar; tartışma turu sayısı ve iki ayrı model ayarı

## At
-
