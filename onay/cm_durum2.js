const isler = ["usta-web-2", "ogrenme-2g", "baslangic-hiz-1"];
const out = {};
for (const i of isler) {
  let ara = null, sonuc = null;
  try { ara = fs.fs_read_text_file({ path: "C:\\Projeler\\omer-skills\\.kos\\kopru\\ara\\" + i + ".md", tail: 6 }).content.slice(-600); } catch (e) { ara = "yok"; }
  try { const j = fs.fs_read_text_file({ path: "C:\\Projeler\\omer-skills\\.kos\\kopru\\ajan-sira\\" + i + (i === "baslangic-hiz-1" ? "-a" : "") + ".json", tail: 3 }).content; sonuc = j.slice(-500); } catch (e) { sonuc = "yok"; }
  out[i] = { ara, sonuc };
}
const log = git.git_git_log({ repo_path: "C:\\Projeler\\omer-skills", max_count: 15 });
const s = JSON.stringify(log);
out.commitler = (s.match(/(USTA-WEB|OGRENME|BASLANGIC)[^\\"]{0,90}/gi) || []).slice(0, 6);
return out;
