# filesystem (Dey_SBboEte)

**Amaç:** AI agentleri için bağımsız, çalışma ortamları oluşturmak ve verimli depolama sağlamak.
**Araçlar:** LayerFS (Ephemeral Workspaces), Append-only depolama, Auto Checkpoints, Conflict Rules, Recursive Forking, Serverless Store

**Adımlar**
1. [] LayerFS'i kur ve çalışma ortamlarını oluşturmak için kullan.
2. [] Her agentin kendi çalışma ortamını forklayarak oluştur.
3. [] Agentlerin yaptığı değişiklikleri checkpoint olarak kaydet.
4. [] Agentlerin çalışmalarını birleştirmek için ortak bir depolama sistemini kullan.
5. [] Agentlerin çalışmalarını test ortamlarında yürüt ve tamamlandığında birleştir.

**Prompt/kod/ayar:** LayerFSxDSH plugin, DeepSeek Harness
**Sonuç:** AI agentleri için bağımsız çalışma ortamları oluşturulur ve verimli depolama sağlanır. 157 snapshot'ın 100MB'de tutulması gibi verimlilik elde edilir.
**Bizde (öneri, modelden):** kurulu araçlarla LayerFS'i kullanarak AI agentleri için bağımsız çalışma ortamları oluşturabilir ve verimli depolama sağlayabilirsiniz.
**Daha iyi (öneri):** LayerFS'i daha geniş bir AI agentleri ekosistemine entegre ederek, daha karmaşık senaryolar için optimize edilebilir.
