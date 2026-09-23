# ONAY ornek

Katman T2 · fixture (14b canlı `video onay ornek --kuru`); gerçek paket değil, koşulmaz.

## Kurulum
- npm: ornek-cli@1.2.3
- mcp: ornek --env ORNEK_KEY=${ORNEK_KEY} -- npx -y ornek-mcp@1.2.3

## Duman testi
- komut: ornek-cli --version
- cikis: 0
- desen: \d+\.\d+\.\d+

## Geri alma
- mcp: ornek
- npm: ornek-cli

## Köprü izni
- arac: ornek-cli
- altIzin: --version, list

## Ayar
- env.ORNEK_KEY: ${ORNEK_KEY}
- skillOverrides.ornek: "on"
