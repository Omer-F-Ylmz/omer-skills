import sys
sys.path.insert(0, "tools")
from mem_fix_omni import ZINCIR, serbest_mi


def test_ucretli_openrouter_reddedilir():
    assert not serbest_mi("openrouter/openai/gpt-oss-20b")
    assert serbest_mi("openrouter/nvidia/nemotron-3.5-lightning:free")
    assert serbest_mi("groq/openai/gpt-oss-20b")


def test_zincir_temiz():
    assert all(serbest_mi(m) for m in ZINCIR)
