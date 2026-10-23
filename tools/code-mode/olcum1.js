const R = "C:\\Projeler\\omer-skills";
const st = git.git_git_status({ repo_path: R });
const lg = git.git_git_log({ repo_path: R, max_count: 25 });
const df = git.git_git_diff_unstaged({ repo_path: R });
const s = x => typeof x === "string" ? x : JSON.stringify(x);
return { ham_karakter: { status: s(st).length, log: s(lg).length, diff: s(df).length } };
