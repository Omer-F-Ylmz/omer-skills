const r = fs.fs_read_text_file({ path: "C:\\Projeler\\omer-skills\\.kos\\kopru\\ajan-sira.log", tail: 400 });
const metin = (r && r.content) ? r.content : (typeof r === "string" ? r : JSON.stringify(r));
const satir = metin.split("\n");
const isler = ["code-mode-ab-1", "baslangic-hiz-1", "skill-dogrula-2-a2", "usta-web-2", "ogrenme-2g", "kurulum-dalgasi-2c"];
const son = {};
for (const i of isler) son[i] = satir.filter(l => l.includes(i)).slice(-2).map(l => l.slice(0, 220));
const yenile = satir.filter(l => /YEN[Iİ]LE/.test(l)).slice(-1).map(l => l.slice(0, 200));
return { son_satir: satir.slice(-6).map(l => l.slice(0, 200)), yenile, son };
