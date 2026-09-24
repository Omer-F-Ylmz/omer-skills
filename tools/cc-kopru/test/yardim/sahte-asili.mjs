/** Hiç cevap vermeyen, stdin kapansa da kapanmayan sunucu: zaman aşımı ve ağaç kapanışı testi. */
process.stderr.write(`ASILI_PID=${process.pid}\n`);
process.stdin.resume();
setInterval(() => {}, 1000);
