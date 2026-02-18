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

CITIES = {
    "а": a_ua,
    "б": b_ua,
    "в": v_ua,
    "г": g_ua,
    "ґ": ge_ua,
    "д": d_ua,
    "е": e_ua,
    "є": ye_ua,
    "ж": zh_ua,
    "з": z_ua,
    "і": i_ua,
    "ї": yi_ua,
    "й": j_ua,
    "к": k_ua,
    "л": l_ua,
    "м": m_ua,
    "н": n_ua,
    "о": o_ua,
    "п": p_ua,
    "р": r_ua,
    "с": s_ua,
    "т": t_ua,
    "у": u_ua,
    "ф": f_ua,
    "х": kh_ua,
    "ц": ts_ua,
    "ч": ch_ua,
    "ш": sh_ua,
    "щ": shch_ua,
    "ю": yu_ua,
    "я": ya_ua,
}

if __name__ == "__main__":
    from games.cities.utils import normalised

    for key, value in normalised(CITIES).items():
        print(f"{key}: {value}")
