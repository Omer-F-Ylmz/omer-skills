# 🕸️LangGraph is the framework serious teams reach for when a simple chain is not 
## Künye
🕸️LangGraph is the framework serious teams reach for when a simple chain is not  · fullstackparody · süre: 0:00 · ? · https://www.instagram.com/p/DcWDpKejYOE/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-33 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 32948 tk · claude-haiku-5-5: claude-haiku-5-5 · 43201 tk
## Özet
@fullstackparody'nin 9 sayfalık Instagram carousel'i: LangGraph (LangChain'in düşük seviyeli, durumlu ajan orkestrasyon çatısı, v1.0) için kurulum rehberi. Ajanın State, Node ve Edge'lerden oluşan bir graf olduğunu, add_messages reducer'ını, koşullu kenarları, MemorySaver checkpointer'ını (thread_id) ve create_react_agent ile yaklaşık on satırda araç kullanan ajanı anlatır. Son kare pip install ve python agent.py çıktısını gösterir. Süre 0:00, altyazı yok; kanıtlar kare ve açıklamadan.
## Bölümler
- 0:00 Kapak: LangGraph kurulum rehberi (kare 1)
- 0:00 LangGraph nedir? v1.0, 38K+ yıldız (kare 2)
- 0:00 Mimari: ajan bir graf (kare 3)
- 0:00 State: tek paylaşılan bellek (kare 4)
- 0:00 Node ve Edge ile akış kontrolü (kare 5)
- 0:00 Bellek: checkpointer ve thread_id (kare 6)
- 0:00 Hızlı yol: create_react_agent (kare 7)
- 0:00 Kurulum ve çalıştırma (kare 8)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| LangGraph | yok | teknik | yok | LangChain'in durumlu ajanları graf olarak kuran düşük seviyeli orkestrasyon çatısı. | 0:00 | Kapak ve genel bakış kareleri LangGraph'i tanıtıyor. (karede: Kare 1'de büyük 'LangGraph' başlığı ve 'The Complete Setup Guide'; kare 2'de 'What is LangGraph?'.) |
| LangChain | yok | teknik | yok | LangGraph'in bakımını yapan çatı; ayrıca langchain_core ve langchain-openai paketleri. | 0:00 | 'From LangChain, now at v1.0.' (karede: Kare 2: 'From LangChain, now at v1.0.'; kare 7'de 'from langchain_core.tools import tool'.) |
| StateGraph | yok | teknik | yok | Graf oluşturucu sınıf; builder = StateGraph(State). | 0:00 | Kod satırı 'builder = StateGraph(State)'. (karede: Kare 5: 'from langgraph.graph import StateGraph, START, END' ve 'builder = StateGraph(State)'.) |
| add_messages | yok | teknik | yok | Mesajları üzerine yazmak yerine ekleyen reducer. | 0:00 | 'add_messages just appends instead of overwriting.' (karede: Kare 4: state.py'de 'messages: Annotated[list, add_messages]' ve add_messages daire içine alınmış.) |
| Koşullu kenar | yok | teknik | yok | State'e göre yönlendiren add_conditional_edges; döngü ve dallanma sağlar. | 0:00 | builder.add_conditional_edges('agent', should_continue) · kanıt: kare (karede: Kare 5 satır 8 add_conditional_edges; kare 3 diyagramında 'conditional edge' etiketi.) |
| MemorySaver | yok | teknik | yok | Bellek içi checkpointer; thread_id ile durumu her adımda kaydeder. | 0:00 | checkpointer = MemorySaver() (karede: Kare 6: 'from langgraph.checkpoint.memory import MemorySaver', 'thread_id' daire içinde, 'user-001'.) |
| SQLite | yok | teknik | yok | Üretimde MemorySaver yerine önerilen kalıcı checkpointer deposu. | 0:00 | 'Swap MemorySaver for SQLite or Postgres in production.' (karede: Kare 6 metni: 'Swap MemorySaver for SQLite or Postgres in production.') |
| Postgres | yok | teknik | yok | Üretimde MemorySaver yerine önerilen kalıcı checkpointer deposu. | 0:00 | 'Swap MemorySaver for SQLite or Postgres in production.' (karede: Kare 6 metni: 'Swap MemorySaver for SQLite or Postgres in production.') |
| create_react_agent | yok | teknik | yok | Model ve araç listesinden hazır araç kullanan ajan grafı kurar. | 0:00 | 'create_react_agent builds a full tool-using agent for you.' (karede: Kare 7: 'from langgraph.prebuilt import create_react_agent' ve 'agent = create_react_agent(model, [multiply])'.) |
| ChatOpenAI | yok | teknik | yok | langchain_openai'den sohbet modeli sarmalayıcısı; ajanın modeli. | 0:00 | model = ChatOpenAI(model='gpt-4o-mini') (karede: Kare 7 satır 1 'from langchain_openai import ChatOpenAI' ve satır 10.) |
| gpt-4o-mini | yok | teknik | yok | Örnek ajanda kullanılan OpenAI modeli. | 0:00 | ChatOpenAI(model='gpt-4o-mini') · kanıt: kare (karede: Kare 7 satır 10: model='gpt-4o-mini'.) |
| langchain-openai | yok | CLI | yok | pip ile LangGraph'le birlikte kurulan OpenAI entegrasyon paketi. | 0:00 | $ pip install -U langgraph langchain-openai (karede: Kare 8 terminal: '$ pip install -U langgraph langchain-openai'.) |
| pip | yok | CLI | yok | Python paket yöneticisi; kurulum komutu. | 0:00 | 'One pip install, then invoke the agent.' (karede: Kare 8: '$ pip install -U langgraph langchain-openai'.) |
| @tool | yok | teknik | yok | langchain_core dekoratörü; Python fonksiyonunu ajan aracına çevirir (multiply). | 0:00 | @tool def multiply(a: float, b: float) -> float (karede: Kare 7: 'from langchain_core.tools import tool' ve '@tool' ile multiply.) |
| TypedDict | yok | teknik | yok | State'i tanımlamak için typing_extensions'tan tipli sözlük. | 0:00 | class State(TypedDict) (karede: Kare 4: 'from typing_extensions import TypedDict' ve 'class State(TypedDict):'.) |
| Python | yok | CLI | yok | Örnek kodun dili; python agent.py ile çalıştırılır. | 0:00 | $ python agent.py (karede: Kare 8: '$ python agent.py' ve çıktı 'agent: 5 times 3 is 15'.) |
| Annotated | yok | teknik | yok | Alan tipine reducer bağlamak için kullanılan Python typing yapısı. | 0:00 | messages: Annotated[list, add_messages] (karede: Kare 4: state.py'de from typing import Annotated satırı ve messages alanı.) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip install -U langgraph langchain-openai | LangGraph ve langchain-openai paketlerini kurar veya günceller. (karede: Kare 8 terminalinde '$ pip install -U langgraph langchain-openai'.) | 0:00 | kare |
| python agent.py | Örnek ajanı çalıştırır; multiply aracını çağırıp 5 çarpı 3 = 15 çıktısı verir. (karede: Kare 8 terminalinde '$ python agent.py', altında 'agent: 5 times 3 is 15' ve '[tools called: multiply]'.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| LangGraph 38K+ yıldıza sahip. | 0:00 | sayısal |
| LangGraph; Klarna, Replit ve Elastic'te üretimde çalışıyor. | 0:00 | özellik |
| LangGraph 1.0 sürümü bu yıl yayımlandı. | açıklama | sayısal |
| Basit bir zincir yetmediğinde ciddi ekipler LangGraph'e yöneliyor. | 0:00 | karşılaştırma |
| Koşullu kenarlar, doğrusal zincirin yapamadığı döngü, dallanma ve yeniden denemeyi sağlar. | açıklama | karşılaştırma |
| Checkpointer ile durum thread bazında saklanır; insan onayı için çalışma ortasında duraklatılabilir. | 0:00 | özellik |
| create_react_agent yaklaşık on satırda çalışan araç kullanan ajan verir. | 0:00 | sayısal |
| Üretimde MemorySaver yerine SQLite veya Postgres kullanılmalı. | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 · 0:00 | LangGraph başlığı, Setup Guide | LangGraph | 'LangGraph — The Complete Setup Guide' |
| kare 1 · 0:00 | @fullstackparody | aday değil: konu dışı | Hesap adı her karenin üstünde |
| kare 2 · 0:00 | LangChain | LangChain | 'From LangChain, now at v1.0.' |
| kare 2 · 0:00 | Klarna | aday değil: konu dışı | 'In production at Klarna, Replit, and Elastic.' |
| kare 2 · 0:00 | Replit | aday değil: konu dışı | Aynı satırda üretim kullanıcısı olarak |
| kare 2 · 0:00 | Elastic | aday değil: konu dışı | Aynı satırda üretim kullanıcısı olarak |
| kare 3 · 0:00 | State, Nodes, Edges | aday değil: başka adayın parçası (LangGraph) | 'Three primitives run everything.' |
| kare 3 · 0:00 | Koşullu kenar diyagramı | Koşullu kenar | Diyagramda 'conditional edge' etiketi |
| kare 4 · 0:00 | TypedDict | TypedDict | class State(TypedDict) |
| kare 4 · 0:00 | typing / Annotated | aday değil: genel kavram | from typing import Annotated |
| kare 4 · 0:00 | add_messages | add_messages | Annotated[list, add_messages] daire içinde |
| kare 5 · 0:00 | StateGraph | StateGraph | builder = StateGraph(State) |
| kare 5 · 0:00 | add_conditional_edges | Koşullu kenar | add_conditional_edges('agent', should_continue) |
| kare 5 · 0:00 | add_node / add_edge / compile | aday değil: başka adayın parçası (StateGraph) | builder.add_node('agent', call_model) |
| kare 6 · 0:00 | MemorySaver / checkpointer | MemorySaver | checkpointer = MemorySaver() |
| kare 6 · 0:00 | thread_id | aday değil: başka adayın parçası (MemorySaver) | config thread_id 'user-001' |
| kare 6 · 0:00 | SQLite | SQLite | 'Swap MemorySaver for SQLite or Postgres' |
| kare 6 · 0:00 | Postgres | Postgres | Aynı cümlede |
| kare 6 · 0:00 | İnsan onayı için duraklatma | aday değil: başka adayın parçası (MemorySaver) | 'pause for human approval mid-run' |
| kare 7 · 0:00 | create_react_agent | create_react_agent | from langgraph.prebuilt import create_react_agent |
| kare 7 · 0:00 | ChatOpenAI | ChatOpenAI | from langchain_openai import ChatOpenAI |
| kare 7 · 0:00 | gpt-4o-mini | gpt-4o-mini | ChatOpenAI(model='gpt-4o-mini') |
| kare 7 · 0:00 | @tool / langchain_core.tools | @tool | @tool def multiply |
| kare 8 · 0:00 | pip install komutu | pip | $ pip install -U langgraph langchain-openai |
| kare 8 · 0:00 | langchain-openai paketi | langchain-openai | pip komutunda paket adı |
| kare 8 · 0:00 | python agent.py | Python | $ python agent.py |
| açıklama | Stateful ajanlar, loop/retry, thread | aday değil: genel kavram | 'loops, branching, and retries a linear chain cannot do' |
| açıklama | LangGraph 1.0 sürümü | LangGraph | 'Version 1.0 shipped this year.' |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamıyor |
| sözlük | React | aday değil: başka adayın parçası (create_react_agent) | Yalnız create_react_agent adında |
| sözlük | Inter | aday değil: konu dışı | Metinde Inter adı yok; yazı tipi doğrulanamadı |
| sözlük | Linear | aday değil: konu dışı | Açıklamada 'linear chain' ifadesi, araç değil |
## Kareden okunanlar
- Kare 1 · 0:00: TUTORIAL · LangGraph · The Complete Setup Guide; START → agent → tools → END diyagramı.
- Kare 2 · 0:00: What is LangGraph? Durumlu AI ajanları için düşük seviyeli çatı, v1.0, 38K+ yıldız; Klarna, Replit, Elastic.
- Kare 3 · 0:00: Your agent is a graph; State, Nodes, Edges; graph.py'de koşullu kenar diyagramı.
- Kare 4 · 0:00: state.py: Annotated, TypedDict, add_messages; class State(TypedDict): messages: Annotated[list, add_messages].
- Kare 5 · 0:00: graph.py: StateGraph(State), add_node agent/tools, add_edge, add_conditional_edges('agent', should_continue), compile().
- Kare 6 · 0:00: memory.py: MemorySaver, compile(checkpointer=checkpointer), config thread_id 'user-001', graph.invoke.
- Kare 7 · 0:00: agent.py: ChatOpenAI, @tool multiply, model='gpt-4o-mini', create_react_agent(model, [multiply]).
- Kare 8 · 0:00: terminal: pip install -U langgraph langchain-openai; python agent.py; 'agent: 5 times 3 is 15'; '[tools called: multiply]'.
## Belirsizlikler
- Video süresi 0:00 (görsel carousel); tüm kare zamanları 0:00 olarak yazıldı.
- OCR 9 görsel listeliyor ama yalnız 8 kare eklendi; 9. sayfa (THE END, 'Nikhil / @fullstackparody') yalnız OCR'dan biliniyor.
- Yorumlar girişsiz alınamadı.
- Yazı tipi aileleri (kalın dar grotesk, italik serif, mono) karede kesin adlandırılamadı; sözlükteki Inter, Linear eşleşmeleri doğrulanamadı, aday yapılmadı.
- Sözlükteki 'React' yalnız create_react_agent adının parçası; ayrı araç değil.
- Klarna, Replit ve Elastic yalnız üretim kullanıcısı olarak anılıyor; kullanılmadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — LangGraph'i ve ajanın graf mimarisini tanıtma: START, agent, tools, END düğümleri — araçlar: LangGraph, LangChain
- 2. adım — State'i TypedDict ve add_messages reducer ile tanımlama (state.py) — araçlar: TypedDict, add_messages
- 3. adım — Node'ları add_node ile ekleme (agent: call_model, tools: tool_node) — araçlar: StateGraph
- 4. adım — Kenarları bağlama: START'tan agent'a, koşullu kenar (should_continue), tools'tan agent'a — araçlar: StateGraph, Koşullu kenar
- 5. adım — Grafı builder.compile() ile derleme — araçlar: StateGraph
- 6. adım — MemorySaver checkpointer ekleyip thread_id ile config oluşturma, graph.invoke çağırma — araçlar: MemorySaver
- 7. adım — Üretim için checkpointer'ı SQLite veya Postgres ile değiştirmeyi önerme — araçlar: SQLite, Postgres
- 8. adım — Hızlı yol: @tool ile multiply aracı yazma — araçlar: @tool, LangChain
- 9. adım — ChatOpenAI modelini gpt-4o-mini ile oluşturma — araçlar: ChatOpenAI, gpt-4o-mini
- 10. adım — create_react_agent(model, [multiply]) ile ajanı kurma — araçlar: create_react_agent
- 11. adım — Paketleri pip ile kurma — araçlar: pip, langchain-openai
- 12. adım — python agent.py ile çalıştırıp çıktıyı doğrulama — araçlar: Python
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
