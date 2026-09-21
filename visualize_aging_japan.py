# /// script
# requires-python = ">=3.11, <3.12"
# dependencies = [
#     "pandas>=2.0.0",
#     "matplotlib>=3.8.0",
#     "japanize-matplotlib>=1.1.3",
#     "setuptools",
# ]
# ///
"""
日本の高齢化と人口推移の可視化スクリプト
- 出典: 総務省統計局「国勢調査」および 国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計・出生中位／死亡中位）」
"""

import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import numpy as np

# データの定義（単位: 万人）
data = {
    "年": [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025, 2030, 2040, 2050, 2060, 2070],
    "年少人口_0_14": [2979, 2807, 2515, 2751, 2249, 1847, 1684, 1503, 1380, 1270, 1073, 955, 852, 797],
    "生産年齢人口_15_64": [5017, 6047, 7212, 7883, 8590, 8622, 8103, 7509, 7150, 6766, 5978, 5275, 4793, 4529],
    "前期高齢者_65_74": [311, 386, 515, 698, 893, 1300, 1506, 1743, 1498, 1428, 1680, 1555, 1500, 1167],
    "後期高齢者_75以上": [105, 149, 224, 367, 597, 901, 1419, 1860, 2179, 2288, 2248, 2285, 2364, 2200],
}

df = pd.DataFrame(data)

# 計算項目
df["高齢者人口_計"] = df["前期高齢者_65_74"] + df["後期高齢者_75以上"]
df["総人口"] = df["年少人口_0_14"] + df["生産年齢人口_15_64"] + df["高齢者人口_計"]
df["高齢化率"] = (df["高齢者人口_計"] / df["総人口"]) * 100
df["現役世代支え人数"] = df["生産年齢人口_15_64"] / df["高齢者人口_計"]

# プロット設定
if "seaborn-v0_8-whitegrid" in plt.style.available:
    plt.style.use("seaborn-v0_8-whitegrid")
else:
    plt.style.use("default")

# style.use でリセットされたフォントを日本語対応フォントに再適用
japanize_matplotlib.japanize()
fig = plt.figure(figsize=(15, 12), dpi=150)
fig.patch.set_facecolor("#FAFAFC")

# 2行1列のサブプロット構成
gs = fig.add_gridspec(2, 1, height_ratios=[1.3, 1.0], hspace=0.35)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ==============================================================================
# 上段: 人口構成の推移と高齢化率（2軸グラフ）
# ==============================================================================
ax1.set_facecolor("#FFFFFF")

years = df["年"]
p_child = df["年少人口_0_14"]
p_work = df["生産年齢人口_15_64"]
p_young_old = df["前期高齢者_65_74"]
p_old_old = df["後期高齢者_75以上"]

colors = ["#4E79A7", "#59A14F", "#F28E2B", "#E15759"]
labels = ["年少人口（0〜14歳）", "生産年齢人口（15〜64歳）", "前期高齢者（65〜74歳）", "後期高齢者（75歳以上）"]

ax1.stackplot(
    years,
    p_child,
    p_work,
    p_young_old,
    p_old_old,
    labels=labels,
    colors=colors,
    alpha=0.85,
)

# 2020年と2025年の間に実績と将来推計の境界線を描画
ax1.axvline(x=2020, color="#555555", linestyle="--", linewidth=1.5, alpha=0.8)
ax1.text(2018, 12800, "← 実績値", ha="right", va="center", fontsize=11, fontweight="bold", color="#333333")
ax1.text(2022, 12800, "将来推計（社人研 令和5年推計）→", ha="left", va="center", fontsize=11, fontweight="bold", color="#C0392B")

# 右軸に高齢化率の折れ線をプロット
ax1_twin = ax1.twinx()
ax1_twin.grid(False)

# 実績部分（〜2020）と推計部分（2020〜）で線種を分ける
past_mask = df["年"] <= 2020
future_mask = df["年"] >= 2020

ax1_twin.plot(df.loc[past_mask, "年"], df.loc[past_mask, "高齢化率"], color="#800020", linewidth=3.2, label="高齢化率（実績）", marker="o", markersize=6)
ax1_twin.plot(df.loc[future_mask, "年"], df.loc[future_mask, "高齢化率"], color="#800020", linewidth=3.2, linestyle=":", label="高齢化率（推計）", marker="s", markersize=6)

# 高齢化率の主要マイルストーンにアノテーション
milestones = [
    (1970, 7.1, "1970年 7.1%\n【高齢化社会】突入", (1962, 14)),
    (1994, 14.1, "1994年 14.1%\n【高齢社会】へ", (1985, 22)),
    (2007, 21.5, "2007年 21.5%\n【超高齢社会】へ", (1998, 29)),
    (2025, 29.6, "2025年 29.6%\n国民の約3人に1人が高齢者", (2018, 38)),
    (2070, 38.7, "2070年 38.7%\n約2.6人に1人が高齢者", (2055, 45)),
]

for yr, rate, text, xytext in milestones:
    ax1_twin.annotate(
        text,
        xy=(yr, rate),
        xytext=xytext,
        arrowprops=dict(facecolor="#800020", shrink=0.08, width=1.2, headwidth=5, alpha=0.8),
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FFF5F5", ec="#800020", alpha=0.9),
    )

ax1.set_title("日本の人口構成の推移と高齢化率（1950年〜2070年推計）", fontsize=16, fontweight="bold", pad=15, color="#1A1A1A")
ax1.set_ylabel("人口（万人）", fontsize=12, fontweight="bold", color="#333333")
ax1_twin.set_ylabel("高齢化率 65歳以上比率（%）", fontsize=12, fontweight="bold", color="#800020")

ax1.set_xlim(1948, 2072)
ax1.set_ylim(0, 14200)
ax1_twin.set_ylim(0, 52)
ax1.set_xticks(df["年"])
ax1.set_xticklabels([f"{y}年" for y in df["年"]], rotation=35, ha="right")

# 凡例を整理
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.95, edgecolor="#DDDDDD", fontsize=10)

# ==============================================================================
# 下段: 扶養負担の変化（現役世代何人で高齢者1人を支えるか）
# ==============================================================================
ax2.set_facecolor("#FFFFFF")

selected_years = [1960, 1980, 1990, 2000, 2010, 2020, 2025, 2040, 2070]
df_sub = df[df["年"].isin(selected_years)].copy()

# カラーグラデーション（青系から負担重化の赤橙系へ）
bar_colors = [
    "#2E86AB", "#3A9AB7", "#52A9B9", "#72B9B5", "#F6C85F", "#F49E4C", "#E8743B", "#DE425B", "#C02543"
]

x_pos = np.arange(len(df_sub))
bars = ax2.bar(x_pos, df_sub["現役世代支え人数"], color=bar_colors, width=0.55, edgecolor="#333333", linewidth=0.8, alpha=0.9)

ax2.set_title("現役世代の負担変化：高齢者（65歳以上）1人を現役世代（15〜64歳）何人で支えるか", fontsize=15, fontweight="bold", pad=15, color="#1A1A1A")
ax2.set_ylabel("現役世代の人数（人）", fontsize=12, fontweight="bold", color="#333333")
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f"{y}年" for y in df_sub["年"]], fontsize=11, fontweight="bold")
ax2.set_ylim(0, 14.5)

# 各バーの上に人数と解説ラベルを追加（重なりを避ける配置）
callout_info = {
    1960: ("11.3人", "【胴上げ型】\n11.3人で1人を支える", 13.0),
    1980: ("7.4人", None, None),
    1990: ("5.8人", "【騎馬戦型】\n5.8人で1人を支える", 8.8),
    2000: ("3.9人", None, None),
    2010: ("2.8人", None, None),
    2020: ("2.1人", None, None),
    2025: ("1.9人", "2人を切る\n(1.9人)", 4.5),
    2040: ("1.5人", None, None),
    2070: ("1.3人", "【肩車型】\nほぼ1対1 (1.3人)", 4.0),
}

for i, (bar, yr) in enumerate(zip(bars, df_sub["年"])):
    val = df_sub.loc[df_sub["年"] == yr, "現役世代支え人数"].values[0]
    num_txt, desc_txt, callout_y = callout_info[yr]
    
    # バー直上の数値
    ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.25, num_txt, ha="center", va="bottom", fontsize=11, fontweight="bold", color="#111111")
    
    # 特別な吹き出し解説
    if desc_txt is not None:
        ax2.annotate(
            desc_txt,
            xy=(bar.get_x() + bar.get_width() / 2, val + 0.8),
            xytext=(bar.get_x() + bar.get_width() / 2, callout_y),
            ha="center",
            arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
            bbox=dict(boxstyle="square,pad=0.35", fc="#FFFFFF", ec="#555555", lw=0.9),
            fontsize=9.5,
            fontweight="bold",
        )

# 2025年以降の領域を点線で区切る
ax2.axvline(x=5.5, color="#555555", linestyle="--", linewidth=1.5, alpha=0.8)
ax2.text(5.3, 13.2, "← 実績", ha="right", fontsize=10, fontweight="bold", color="#555555")
ax2.text(5.7, 13.2, "将来推計 →", ha="left", fontsize=10, fontweight="bold", color="#C0392B")

# 出典明記
fig.text(0.98, 0.015, "出典：総務省統計局「国勢調査」、国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計）」出生中位・死亡中位仮定", ha="right", fontsize=9, color="#666666")

# 保存
output_filename = "japan_aging_demographics.png"
plt.savefig(output_filename, dpi=200, bbox_inches="tight")
print(f"グラフを正常に保存しました: {output_filename}")
