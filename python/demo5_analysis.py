import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def extract_number(series):
    return series.astype(str).str.extract(r'([-+]?\d*\.?\d+)')[0].astype(float)


def get_numeric(df, col, out_col=None):
    if col not in df.columns:
        raise KeyError(f"Không tìm thấy cột '{col}'. Các cột hiện có: {list(df.columns)}")
    name = out_col or f"{col}_num"
    df[name] = extract_number(df[col])
    return name


def save_plot(path):
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


# Giữ đúng tên CSV do script demo sinh ra.
# Có thể truyền tên file khác khi cần: python demo5_analysis_output-fixed-v2.py ten_file.csv
file = sys.argv[1] if len(sys.argv) > 1 else "demo5_results.csv"
plots_dir = "plots_demo5"
ensure_dir(plots_dir)

# ===== ĐỌC DỮ LIỆU =====
df = pd.read_csv(file, sep=None, engine="python")
df.columns = [c.strip() for c in df.columns]
df["scenario"] = df["scenario"].astype(str).str.strip()

print("File dữ liệu:", file)
print("Các cột đọc được:", df.columns.tolist())
print("Các kịch bản:", df["scenario"].unique())

# ===== CHUẨN HÓA SỐ LIỆU THEO CSV MỚI =====
# CSV mới Demo 5:
# scenario,mode,band,nSta,offeredPerSta,totalOffered,width,mcs,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
get_numeric(df, "band", "band_num")
get_numeric(df, "nSta", "nSta_num")
get_numeric(df, "offeredPerSta", "offered_num")
if "totalOffered" in df.columns:
    get_numeric(df, "totalOffered", "total_offered_num")
else:
    df["total_offered_num"] = df["offered_num"] * df["nSta_num"]
get_numeric(df, "width", "width_num")
get_numeric(df, "thrTotal", "thr_num")
get_numeric(df, "loss", "loss_num")          # CSV mới đã là %
get_numeric(df, "delayMs", "delay_num")
get_numeric(df, "jitterMs", "jitter_num")
get_numeric(df, "efficiency", "eff_num")     # CSV mới đã là %
get_numeric(df, "fairness", "fair_num")

# ===== XUẤT FILE CHUẨN HÓA TÊN CỘT TIẾNG VIỆT KHÔNG DẤU =====
cols_out = [
    "scenario", "mode", "band_num", "nSta_num", "offered_num",
    "total_offered_num", "width_num", "mcs", "thr_num", "loss_num",
    "delay_num", "jitter_num", "eff_num", "fair_num",
]
cols_out = [c for c in cols_out if c in df.columns]

df_out = df[cols_out].rename(columns={
    "scenario": "kich_ban",
    "mode": "che_do",
    "band_num": "bang_tan_GHz",
    "nSta_num": "so_luong_STA",
    "offered_num": "tai_dau_vao_moi_STA_Mbps",
    "total_offered_num": "tong_tai_dau_vao_Mbps",
    "width_num": "do_rong_kenh_MHz",
    "mcs": "MCS",
    "thr_num": "thong_luong_Mbps",
    "loss_num": "ti_le_mat_goi_percent",
    "delay_num": "do_tre_ms",
    "jitter_num": "jitter_ms",
    "eff_num": "hieu_suat_percent",
    "fair_num": "chi_so_cong_bang_Jain",
})

df_out.to_csv("demo5_results_chuan_hoa_tieng_viet.csv", index=False)

# =========================
# 1. SO SÁNH BĂNG TẦN
# =========================
df_band = df[df["scenario"] == "band_compare"].copy().sort_values("band_num")

if not df_band.empty:
    plt.figure()
    plt.bar(df_band["band_num"].astype(int).astype(str), df_band["thr_num"])
    plt.xlabel("Băng tần (GHz)")
    plt.ylabel("Thông lượng tổng (Mbps)")
    plt.title("Thông lượng theo băng tần")
    save_plot(f"{plots_dir}/thong_luong_theo_bang_tan.png")

    plt.figure()
    plt.bar(df_band["band_num"].astype(int).astype(str), df_band["delay_num"])
    plt.xlabel("Băng tần (GHz)")
    plt.ylabel("Độ trễ trung bình (ms)")
    plt.title("Độ trễ theo băng tần")
    save_plot(f"{plots_dir}/do_tre_theo_bang_tan.png")

    plt.figure()
    plt.bar(df_band["band_num"].astype(int).astype(str), df_band["fair_num"])
    plt.xlabel("Băng tần (GHz)")
    plt.ylabel("Chỉ số công bằng Jain")
    plt.title("Công bằng theo băng tần")
    save_plot(f"{plots_dir}/cong_bang_theo_bang_tan.png")

# =========================
# 2. ẢNH HƯỞNG CỦA ĐỘ RỘNG KÊNH
# =========================
df_width = df[df["scenario"] == "width_scaling"].copy().sort_values("width_num")

if not df_width.empty:
    plt.figure()
    plt.plot(df_width["width_num"], df_width["thr_num"], marker="o")
    plt.xlabel("Độ rộng kênh (MHz)")
    plt.ylabel("Thông lượng tổng (Mbps)")
    plt.title("Thông lượng theo độ rộng kênh")
    save_plot(f"{plots_dir}/thong_luong_theo_do_rong_kenh.png")

    plt.figure()
    plt.plot(df_width["width_num"], df_width["delay_num"], marker="o")
    plt.xlabel("Độ rộng kênh (MHz)")
    plt.ylabel("Độ trễ trung bình (ms)")
    plt.title("Độ trễ theo độ rộng kênh")
    save_plot(f"{plots_dir}/do_tre_theo_do_rong_kenh.png")

    plt.figure()
    plt.plot(df_width["width_num"], df_width["fair_num"], marker="o")
    plt.xlabel("Độ rộng kênh (MHz)")
    plt.ylabel("Chỉ số công bằng Jain")
    plt.title("Công bằng theo độ rộng kênh")
    save_plot(f"{plots_dir}/cong_bang_theo_do_rong_kenh.png")

# =========================
# 3. ẢNH HƯỞNG CỦA TẢI ĐẦU VÀO
# =========================
df_load = df[df["scenario"] == "load_sweep"].copy().sort_values("offered_num")

if not df_load.empty:
    plt.figure()
    plt.plot(df_load["offered_num"], df_load["thr_num"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mbps)")
    plt.ylabel("Thông lượng tổng (Mbps)")
    plt.title("Thông lượng theo tải đầu vào")
    save_plot(f"{plots_dir}/thong_luong_theo_tai_dau_vao.png")

    plt.figure()
    plt.plot(df_load["offered_num"], df_load["delay_num"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mbps)")
    plt.ylabel("Độ trễ trung bình (ms)")
    plt.title("Độ trễ theo tải đầu vào")
    save_plot(f"{plots_dir}/do_tre_theo_tai_dau_vao.png")

    plt.figure()
    plt.plot(df_load["offered_num"], df_load["loss_num"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mbps)")
    plt.ylabel("Tỷ lệ mất gói (%)")
    plt.title("Tỷ lệ mất gói theo tải đầu vào")
    save_plot(f"{plots_dir}/mat_goi_theo_tai_dau_vao.png")

# =========================
# 4. ẢNH HƯỞNG CỦA SỐ LƯỢNG STA
# =========================
df_sta = df[df["scenario"] == "sta_scaling"].copy().sort_values("nSta_num")

if not df_sta.empty:
    plt.figure()
    plt.plot(df_sta["nSta_num"], df_sta["thr_num"], marker="o")
    plt.xlabel("Số lượng STA")
    plt.ylabel("Thông lượng tổng (Mbps)")
    plt.title("Thông lượng theo số lượng STA")
    save_plot(f"{plots_dir}/thong_luong_theo_so_luong_sta.png")

    plt.figure()
    plt.plot(df_sta["nSta_num"], df_sta["fair_num"], marker="o")
    plt.xlabel("Số lượng STA")
    plt.ylabel("Chỉ số công bằng Jain")
    plt.title("Công bằng theo số lượng STA")
    save_plot(f"{plots_dir}/cong_bang_theo_so_luong_sta.png")

print(f"DONE! Biểu đồ Demo 5 đã lưu trong thư mục '{plots_dir}'.")
print("File dữ liệu chuẩn hóa: demo5_results_chuan_hoa_tieng_viet.csv")
