const s = git.git_git_status({ repo_path: "C:\\Projeler\\omer-skills" });
const t = gw.time_get_current_time({ timezone: "Europe/Istanbul" });
return { git_status_karakter: JSON.stringify(s).length, saat: JSON.stringify(t).slice(0, 90) };
