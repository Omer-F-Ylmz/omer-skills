# GitHub Actions

- tür: arac · durum: KURULMADI-SIRADA · videolar: DZpySOnOCxI,DatpvftE-Iq,DcNGpmXOR42,DcbDo37zTvJ,DcjEHTvyYBS,Dd40YRPxuEB,Dd9R75ej5jv,DdBGaAgnQyL,DdOhd6bCdSM,DdnQtgBCUZu,DdoRKQUAdeM,DePvqHlDuTU,DeRwKUAsJW9,Detx5PHtW_R,DeyIOlwk0ar,DezcE_BMmrJ,DfBcE4Bli0y,DfFK-iuhm--
- bizde: yok

## Özellikler
- Workflow'lar 'on' tetikleyicileriyle olay güdümlü çalışır; 'jobs' ile paralel görev grupları kurulur
- ci-pr: her pull request'i izole bir GKE namespace'ine deploy edip staging doğrulaması yapar
- ci-main: main'e merge olunca çalışır
- Helm chart, Kustomize build, Kubernetes manifest ve Terraform yapılandırmalarını ayrı ayrı doğrulayan workflow'lar var
- cleanup workflow: merge sonrası PR namespace'lerini siler
- Helm chart, raw manifest'lere göre values.yaml ile yapılandırılabilen templated bir deploy alternatifi sunar

## Videoda yapılış
DcNGpmXOR42 videosunda bir GKE/Terraform projesinde workflow'ların rolü anlatılıyor; kurulum adımı ya da komut gösterilmiyor. DZpySOnOCxI videosunda ECC repo'su (affaan-m/ECC) linki verilip 28 subagent, 119 skill, 60 slash command iddiası var; bu iddianın GitHub Actions ile ilişkisi transkriptte net değil.

## Bizdeki karşılık ve fark
yok

## Al
PR başına izole namespace ile merge sonrası temizlik workflow'u; ci-pr ve ci-main'in ayrı akışlara bölünmesi

## At
-
