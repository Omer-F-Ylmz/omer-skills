---
name: departman-surec-git-yayin
description: "Git ve yayın müdürü: commit, PR, CI, deploy, canary ve kapanış sırası. Commit, push, ship ya da deploy adımında oku."
---

# Departman: surec-git-yayin — iş sırası

Katalog: `docs/departmanlar/surec-git-yayin.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

## Adımlar
1. **Dal** — yalıtım gerekirse `using-git-worktrees`; akış kuralları `git-workflow-and-versioning`.
2. **Commit** — `commit-commands` (kırmızı ve yeşil ayrı commit); push öncesi `departman-guvenlik` adım 1.
3. **CI** — `ci-cd-and-automation`; kırmızı CI'da yayın yok.
4. **Yayın** — `ship` / `land-and-deploy`; Vercel `deploy-to-vercel`; yayın sonrası `canary`.
5. **Kapanış** — `finishing-a-development-branch`; rapor ≤15 satır (commit · test · CI · sapma), omer-kurallar:15.

## Kapılar
- Kullanıcı istemeden push/deploy yok; default dalda önce dal aç.
- Sır taraması temiz olmadan push yok.
- Paralel ajan kolunda her commit `git commit --trailer "Gorev: <AD>"` taşır; birleştirmede "zaten var/özdeş" iddiası `git cherry -v main <kol>` ile (patch-id; `-` = içerikçe main'de) kanıtlanır, rapora commit → görev satırı (KAYNAK-5, Atlas).

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- hetzner-deploy (1): hetzner-deploy · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:git-cakisma-cozucu
ajan:git-canary-izleme
ajan:git-ci-boru-hatti
ajan:git-commit-mesaji
ajan:git-dal-stratejisi
ajan:git-issue-triyaj
ajan:git-yayin-oncesi-kontrol
ajan:oyn-mod-birlestirici: two mods conflict
### yalnız Claude Code
blueprint: 1行の目的を複数セッション、複数エージェントエンジニアリングプロジェクト向けのステップバイステップ構築計画に変換します。各ステップには自己完結型コンテキストブリーフがあり、新しいエージェントがそれをコールドで実行できます。 敵対的なレビューゲート、依存グラフ、平行ステップ検出、アンチパターンカタログ、計画変更プロトコルを含みます。 トリガー：ユーザーが複雑なマルチPRタスク用の計画、ブループリント、またはロードマップをリクエストするか、複数のセッションが必要な作業を説明する場合。 トリガーしない場合：タスクが単一のPRまたは3未満のツール呼び出しで完成可能な場合、またはユーザーが「単にやってくれ」と言う場合。
convex-self-heal: Production error → triaged, root-caused, repaired, and certified
eas-app-stores: eas.json setup, release pipelines, signing, app versions and
finetuning: : fine-tune, SFT, DPO, RFT, training data, grader
k2: stream setup, producing from Workers or HTTP, configuring
parallel-execution-optimizer: 当用户希望通过并行工作、并发 agents、批量工具调用、隔离 worktree 或多条独立验证通道来大幅加速任务、同时不损失正确性时使用。
preset: : quick deployment, optimal region, best region, automatic
qmd-paket: qmd: dokümanlar ve bilgi tabanı için yerel arama
terminal-ops: ECCのための証拠優先のリポジトリ実行ワークフロー。ユーザーがコマンドの実行、リポジトリの確認、CIの失敗のデバッグ、正確な実行と検証の証明を伴う狭い修正のプッシュを必要とする場合に使用する。
unified-notifications-ops: GitHub、Linear、デスクトップアラート、フック、接続された通信インターフェースを網羅する、統合されたECCネイティブワークフローとして通知を運用する。真の問題がアラートルーティング、重複排除、エスカレーション、またはインボックス崩壊である場合に使用する。
<!-- dizin:son -->
