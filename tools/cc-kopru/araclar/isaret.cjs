// Suit işareti: suit.mjs NODE_OPTIONS=--require ile her node alt sürecine yükler;
// CC_KOPRU_SUIT_ISARET dizinine bu sürecin pid'i düşer, suit sonunda canlılar sayılır.
const dizin = process.env.CC_KOPRU_SUIT_ISARET;
if (dizin) {
  try {
    require("node:fs").writeFileSync(require("node:path").join(dizin, String(process.pid)), "");
  } catch { /* işaret yazılamazsa süreç yine koşar; sayım eksik kalır */ }
}
