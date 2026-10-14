# lab · GPGPU parçacık bulutu (ref activetheory · eşleşme ~8)
Demo `labs/parcacik/` · modül `tools/site-kit/sablon/src/sahne/parcacik.js`.
- Mekanizma: GPUComputationRenderer konum/hız dokuları (ping-pong), girdaplı yükselen alan (buhar/telve tozu), ömür bitince kaynağa dönüş; Points shader konumu dokudan okur, boyut 1/derinlik, ömür boyu sin solması, derinlik sisi.
- Parametre: 256² (65k) yüksek, 96² (9k) düşük kademe; additive blend.
- Bütçe: her iki kademede 60 fps sürekli döngü (RTX 4070 Ti).
- Tuzak: konum dokusu float RT ister (mobilde `EXT_color_buffer_float` yoksa half-float, doğrulanmadı); additive + sis → sis rengini arka planla eşle.
- Mobil düşüş: 96² (ölçüldü 60 fps masaüstü; mobil cihazda ölçülmedi).
