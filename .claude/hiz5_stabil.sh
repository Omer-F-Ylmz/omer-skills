cd /c/Projeler/omer-skills
export VD_GROQ=1 VD_GROQ_MODELLER=whisper-large-v3 VD_GROQ_SAAT=100000 PYTHONIOENCODING=utf-8
for n in 1 2 3; do python tools/video_hiz4_olc.py kos h5_st$n --es 3 > .claude/hiz5_st$n.out 2>&1; done
python tools/video_hiz4_olc.py kos h5_st120 --es 3 --liste .kos/kopru/ogren/hiz4/s120c.txt > .claude/hiz5_st120.out 2>&1
echo BITTI > .claude/hiz5_stabil.bitti
