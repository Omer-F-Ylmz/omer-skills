"""MOTOR-M4c: birleşim tekilleştirme + doğrulama süzgeci."""
import olcum_m4c as o


def test_birlesim_tekil_ve_dogrulama():
    a = {"esl": {0: 0}, "sinif": ["dayanıyor"], "anah": [{"x"}]}
    b = {"esl": {0: 0, 1: 1}, "sinif": ["dayanıyor", "dayanıyor", "dayanmıyor", "ölçülemedi"], "anah": [{"x"}, {"y"}, {"z"}, set()]}
    k, s, e = o.birlesim(a, b, False)
    assert k == {0, 1} and e == [1, 2, 3] and s.count("dayanmıyor") == 1  # 0. kalem kopya (anahtar x)
    k, s, e = o.birlesim(a, b, True)
    assert k == {0, 1} and e == [1] and s == ["dayanıyor", "dayanıyor"]  # dayanmayan/ölçülemedi ek girmez
    b2 = {**b, "anah": [set(), {"y"}, {"z"}, set()]}
    assert 0 not in o.birlesim(a, b2, False)[2]  # anahtarsız ama A'nın yakaladığı altına eşleşen → kopya
