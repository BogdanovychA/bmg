# -*- coding: utf-8 -*-

from .cities.a_ua import a_ua  # "а"
from .cities.b_ua import b_ua  # "б"
from .cities.ch_ua import ch_ua  # "ч"
from .cities.d_ua import d_ua  # "д"
from .cities.e_ua import e_ua  # "е"
from .cities.f_ua import f_ua  # "ф"
from .cities.g_ua import g_ua  # "г"
from .cities.ge_ua import ge_ua  # "ґ"
from .cities.i_ua import i_ua  # "і"
from .cities.j_ua import j_ua  # "й"
from .cities.k_ua import k_ua  # "к"
from .cities.kh_ua import kh_ua  # "х"
from .cities.l_ua import l_ua  # "л"
from .cities.m_ua import m_ua  # "м"
from .cities.n_ua import n_ua  # "н"
from .cities.o_ua import o_ua  # "о"
from .cities.p_ua import p_ua  # "п"
from .cities.r_ua import r_ua  # "р"
from .cities.s_ua import s_ua  # "с"
from .cities.sh_ua import sh_ua  # "ш"
from .cities.shch_ua import shch_ua  # "щ"
from .cities.t_ua import t_ua  # "т"
from .cities.ts_ua import ts_ua  # "ц"
from .cities.u_ua import u_ua  # "у"
from .cities.v_ua import v_ua  # "в"
from .cities.ya_ua import ya_ua  # "я"
from .cities.ye_ua import ye_ua  # "є"
from .cities.yi_ua import yi_ua  # "ї"
from .cities.yu_ua import yu_ua  # "ю"
from .cities.z_ua import z_ua  # "з"
from .cities.zh_ua import zh_ua  # "ж"

NORMALISED = {
    "а": set(map(str.lower, a_ua)),
    "б": set(map(str.lower, b_ua)),
    "в": set(map(str.lower, v_ua)),
    "г": set(map(str.lower, g_ua)),
    "ґ": set(map(str.lower, ge_ua)),
    "д": set(map(str.lower, d_ua)),
    "е": set(map(str.lower, e_ua)),
    "є": set(map(str.lower, ye_ua)),
    "ж": set(map(str.lower, zh_ua)),
    "з": set(map(str.lower, z_ua)),
    "і": set(map(str.lower, i_ua)),
    "ї": set(map(str.lower, yi_ua)),
    "й": set(map(str.lower, j_ua)),
    "к": set(map(str.lower, k_ua)),
    "л": set(map(str.lower, l_ua)),
    "м": set(map(str.lower, m_ua)),
    "н": set(map(str.lower, n_ua)),
    "о": set(map(str.lower, o_ua)),
    "п": set(map(str.lower, p_ua)),
    "р": set(map(str.lower, r_ua)),
    "с": set(map(str.lower, s_ua)),
    "т": set(map(str.lower, t_ua)),
    "у": set(map(str.lower, u_ua)),
    "ф": set(map(str.lower, f_ua)),
    "х": set(map(str.lower, kh_ua)),
    "ц": set(map(str.lower, ts_ua)),
    "ч": set(map(str.lower, ch_ua)),
    "ш": set(map(str.lower, sh_ua)),
    "щ": set(map(str.lower, shch_ua)),
    "ю": set(map(str.lower, yu_ua)),
    "я": set(map(str.lower, ya_ua)),
}

if __name__ == "__main__":
    print("NORMALISED:")
    for key, value in NORMALISED.items():
        print(f"{key}: {value}")
