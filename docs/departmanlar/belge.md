# Departman: belge

> Belge üretimi: docx, pptx, pdf, xlsx, sunum, rapor, diyagram, yazı düzeltme.

Müdür: `departman-belge`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| humanizer | plugin | Rewrite AI-sounding text so it reads naturally without changing what it says. | - | Yayın sonrası |
| agent-skills:documentation-and-adrs | skill | Records decisions and documentation. | Use when you need to document an architecture decision (ADR) or the reasoning behind a de… | Biçim |
| anthropic-skills:departman-belge | skill | Belge müdürü: docx/pptx/pdf/xlsx, rapor ve doküman üretim sırası. | - | - |
| anthropic-skills:humanizer | skill | Rewrite AI-sounding text so it reads like the writer, without changing meaning. | Use for prose with AI tells: forced contrasts, staged openers, stock words, bold labels, … | Yayın sonrası |
| anthropic-skills:writing-guidelines | skill | Review docs or prose for Writing Guidelines compliance. | Use when asked to review my docs, check writing style, audit prose, or check a page again… | Yayın sonrası |
| claude-mem:timeline-report | skill | Generate a "Journey Into [Project]" narrative report analyzing a project's entire develop… | Use when asked for a timeline report, project history analysis, develo | - |
| claude-mem:weekly-digests | skill | Generate a serial week-by-week narrative digest of a project's full claude-mem timeline. | - | - |
| claude-mem:wowerpoint | skill | Turn one document into a kawaii NotebookLM slide-deck PDF. | Use for "wowerpoint this", "make a deck about <file>", "turn this report into slides", or… | Dil |
| diagram | skill | Turn an English description (or mermaid source) into a diagram triplet: the source, an ed… | - | Dil |
| document-generate | skill | Generate missing documentation from scratch for a feature, module, or entire project. | - | Biçim |
| document-release | skill | Post-ship documentation update. | - | - |
| example-skills:doc-coauthoring | skill | Guide users through a structured workflow for co-authoring documentation. | Use when user wants to write documentation, proposals, technical specs, decision docs, or… | Biçim |
| example-skills:internal-comms | skill | A set of resources to help me write all kinds of internal communications, using the forma… | use this skill whenever asked to write some sort of internal com | - |
| make-pdf | skill | Turn any markdown file into a publication-quality PDF. | - | Dil |

## Elle
