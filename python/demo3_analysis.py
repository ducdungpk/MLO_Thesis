import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def ensure_dir(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)


def extract_number(series: pd.Series) -> pd.Series:
    """Hỗ trợ cả CSV sạch và CSV cũ dạng key=value."""
    return series.astype(str).str.extract(r"([-+]?\d*\.?\d+)")[0].astype(float)


def get_required_column(df: pd.DataFrame, candidates: list[str], display_name: str) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(
        f"Không tìm thấy cột {display_name}. Các cột hiện có: {list(df.columns)}"
    )


# ===== LOAD DATA =====
# Giữ đúng tên CSV cũ do script demo sinh ra; có thể truyền tên khác bằng argv[1]
file = sys.argv[1] if len(sys.argv) > 1 else "demo3_results.csv"
df = pd.read_csv(file, sep=None, engine="python")

# ===== CLEAN COLUMNS =====
df.columns = [c.strip() for c in df.columns]
df["scenario"] = df["scenario"].astype(str).str.strip()

print("Các cột đọc được:", df.columns.tolist())
print("Các kịch bản:", df["scenario"].unique())

ensure_dir("plots_demo3")

# ===== COLUMN MAPPING FOR NEW CSV FORMAT =====
nsta_col = get_required_column(df, ["nSta"], "số lượng STA")
offered_col = get_required_column(df, ["offeredPerSta", "offered"], "tải đầu vào mỗi STA")
total_offered_col = "totalOffered" if "totalOffered" in df.columns else None
thr_col = get_required_column(df, ["thrTotal", "throughput", "total"], "thông lượng tổng")
loss_col = get_required_column(df, ["loss"], "tỷ lệ mất gói")
delay_col = get_required_column(df, ["delayMs"], "độ trễ")
jitter_col = get_required_column(df, ["jitterMs"], "jitter")
eff_col = get_required_column(df, ["efficiency"], "hiệu suất")
fair_col = get_required_column(df, ["fairness"], "chỉ số công bằng")

# ===== PARSE NUMERIC DATA =====
df["so_luong_sta"] = extract_number(df[nsta_col])
df["tai_moi_sta_mbps"] = extract_number(df[offered_col])
if total_offered_col:
    df["tong_tai_dau_vao_mbps"] = extract_number(df[total_offered_col])
else:
    df["tong_tai_dau_vao_mbps"] = df["so_luong_sta"] * df["tai_moi_sta_mbps"]
df["thong_luong_mbps"] = extract_number(df[thr_col])
df["mat_goi_phan_tram"] = extract_number(df[loss_col])
df["do_tre_ms"] = extract_number(df[delay_col])
df["jitter_ms"] = extract_number(df[jitter_col])
df["hieu_suat_phan_tram"] = extract_number(df[eff_col])
df["cong_bang_jain"] = extract_number(df[fair_col])

# Xuất thêm file chuẩn hóa tiếng Việt không dấu, dễ dùng cho báo cáo
cols_vi = [
    "scenario",
    "so_luong_sta",
    "tai_moi_sta_mbps",
    "tong_tai_dau_vao_mbps",
    "thong_luong_mbps",
    "mat_goi_phan_tram",
    "do_tre_ms",
    "jitter_ms",
    "hieu_suat_phan_tram",
    "cong_bang_jain",
]
df[cols_vi].to_csv("demo3_results_chuan_hoa_tieng_viet.csv", index=False)

# ===== FILTER SCENARIOS =====
df_load = df[df["scenario"] == "load_sweep"].copy()
df_sta = df[df["scenario"] == "sta_scaling"].copy()

print("Số dòng load_sweep:", len(df_load))
print("Số dòng sta_scaling:", len(df_sta))

# =========================
# 1) Thông lượng theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_moi_sta_mbps"], df_load["thong_luong_mbps"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
plt.ylabel("Thông lượng tổng (Mb/s)")
plt.title("Thông lượng theo tải đầu vào - đơn liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/thong_luong_theo_tai_dau_vao.png")
plt.close()

# =========================
# 2) Độ trễ theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_moi_sta_mbps"], df_load["do_tre_ms"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo tải đầu vào - đơn liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/do_tre_theo_tai_dau_vao.png")
plt.close()

# =========================
# 3) Tỷ lệ mất gói theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_moi_sta_mbps"], df_load["mat_goi_phan_tram"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
plt.ylabel("Tỷ lệ mất gói (%)")
plt.title("Tỷ lệ mất gói theo tải đầu vào - đơn liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/mat_goi_theo_tai_dau_vao.png")
plt.close()

# =========================
# 4) Công bằng theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_moi_sta_mbps"], df_load["cong_bang_jain"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Công bằng theo tải đầu vào - đơn liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/cong_bang_theo_tai_dau_vao.png")
plt.close()

# =========================
# 5) Thông lượng theo số lượng STA
# =========================
plt.figure()
plt.plot(df_sta["so_luong_sta"], df_sta["thong_luong_mbps"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Thông lượng tổng (Mb/s)")
plt.title("Thông lượng theo số lượng STA - đơn liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/thong_luong_theo_so_luong_sta.png")
plt.close()

# =========================
# 6) Công bằng theo số lượng STA
# =========================
plt.figure()
plt.plot(df_sta["so_luong_sta"], df_sta["cong_bang_jain"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Công bằng theo số lượng STA - đơn liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/cong_bang_theo_so_luong_sta.png")
plt.close()

# =========================
# 7) Độ trễ theo số lượng STA
# =========================
plt.figure()
plt.plot(df_sta["so_luong_sta"], df_sta["do_tre_ms"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo số lượng STA - đơn liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/do_tre_theo_so_luong_sta.png")
plt.close()

# =========================
# 8) Hiệu suất theo số lượng STA
# =========================
plt.figure()
plt.plot(df_sta["so_luong_sta"], df_sta["hieu_suat_phan_tram"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Hiệu suất (%)")
plt.title("Hiệu suất theo số lượng STA - đơn liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo3/hieu_suat_theo_so_luong_sta.png")
plt.close()

print("HOÀN TẤT! Biểu đồ Demo 3 đã lưu trong thư mục plots_demo3/")
print("Đã lưu dữ liệu chuẩn hóa: demo3_results_chuan_hoa_tieng_viet.csv")
