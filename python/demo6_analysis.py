import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def extract_number(series):
    """Tách số từ cột CSV, hỗ trợ cả CSV sạch và dạng key=value cũ."""
    return series.astype(str).str.extract(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')[0].astype(float)


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def require_columns(df, required):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(
            "Thiếu cột trong file CSV: " + ", ".join(missing) +
            "\nCác cột hiện có: " + ", ".join(df.columns)
        )


# ===== LOAD DATA =====
# Giữ đúng tên file CSV cũ do run_demo_6.sh sinh ra.
file = sys.argv[1] if len(sys.argv) > 1 else "demo6_results.csv"
df = pd.read_csv(file, sep=None, engine="python")

# Chuẩn hóa tên cột và scenario
df.columns = [c.strip() for c in df.columns]
require_columns(
    df,
    [
        "scenario", "mode", "split", "nSta", "offeredPerSta", "totalOffered",
        "thr5", "thr6", "thrTotal", "loss", "delayMs", "jitterMs",
        "efficiency", "fairness"
    ]
)

df["scenario"] = df["scenario"].astype(str).str.strip()

print("Columns:", df.columns.tolist())
print("Scenarios:", df["scenario"].unique())

ensure_dir("plots_demo6")

# =========================
# PARSE DATA
# =========================
df["mode_num"] = extract_number(df["mode"])
df["split_num"] = extract_number(df["split"])
df["nSta_num"] = extract_number(df["nSta"])
df["offered_num"] = extract_number(df["offeredPerSta"])
df["total_offered_num"] = extract_number(df["totalOffered"])

df["thr5_num"] = extract_number(df["thr5"])
df["thr6_num"] = extract_number(df["thr6"])
df["thr_num"] = extract_number(df["thrTotal"])

df["loss_num"] = extract_number(df["loss"])
df["delay_num"] = extract_number(df["delayMs"])
df["jitter_num"] = extract_number(df["jitterMs"])
df["eff_num"] = extract_number(df["efficiency"])
df["fair_num"] = extract_number(df["fairness"])

# Xuất thêm bảng chuẩn hóa với tên cột tiếng Việt không dấu để dễ đưa vào báo cáo/code.
df_vi = pd.DataFrame({
    "kich_ban": df["scenario"],
    "che_do": df["mode_num"],
    "ty_le_chia_vao_5ghz": df["split_num"],
    "so_luong_sta": df["nSta_num"],
    "tai_moi_sta_mbps": df["offered_num"],
    "tong_tai_dau_vao_mbps": df["total_offered_num"],
    "thong_luong_5ghz_mbps": df["thr5_num"],
    "thong_luong_6ghz_mbps": df["thr6_num"],
    "tong_thong_luong_mbps": df["thr_num"],
    "ty_le_mat_goi_phan_tram": df["loss_num"],
    "do_tre_ms": df["delay_num"],
    "jitter_ms": df["jitter_num"],
    "hieu_suat_phan_tram": df["eff_num"],
    "chi_so_cong_bang": df["fair_num"],
})
df_vi.to_csv("demo6_results_chuan_hoa_tieng_viet.csv", index=False)

# =========================
# 1. SO SÁNH CHẾ ĐỘ
# =========================
df_mode = df[df["scenario"] == "mode_compare"].copy().sort_values("mode_num")

mode_labels = {
    0.0: "Đơn liên kết",
    1.0: "Đa liên kết cân bằng",
    2.0: "Điều phối lưu lượng",
}
mode_x = [mode_labels.get(float(m), str(m)) for m in df_mode["mode_num"]]

plt.figure()
plt.bar(mode_x, df_mode["thr_num"])
plt.xlabel("Chế độ hoạt động")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo chế độ hoạt động")
plt.grid(axis="y")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig("plots_demo6/thong_luong_theo_che_do.png")
plt.close()

plt.figure()
plt.bar(mode_x, df_mode["delay_num"])
plt.xlabel("Chế độ hoạt động")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo chế độ hoạt động")
plt.grid(axis="y")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig("plots_demo6/do_tre_theo_che_do.png")
plt.close()

plt.figure()
plt.bar(mode_x, df_mode["fair_num"])
plt.xlabel("Chế độ hoạt động")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Mức độ công bằng theo chế độ hoạt động")
plt.grid(axis="y")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig("plots_demo6/cong_bang_theo_che_do.png")
plt.close()

# =========================
# 2. QUÉT TỶ LỆ PHÂN PHỐI LƯU LƯỢNG
# =========================
df_split = df[df["scenario"] == "split_sweep"].copy().sort_values("split_num")

plt.figure()
plt.plot(df_split["split_num"], df_split["thr_num"], marker="o")
plt.xlabel("Tỷ lệ lưu lượng đưa vào liên kết 5 GHz")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo tỷ lệ phân phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/thong_luong_theo_ty_le_phan_phoi.png")
plt.close()

plt.figure()
plt.plot(df_split["split_num"], df_split["delay_num"], marker="o")
plt.xlabel("Tỷ lệ lưu lượng đưa vào liên kết 5 GHz")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo tỷ lệ phân phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/do_tre_theo_ty_le_phan_phoi.png")
plt.close()

plt.figure()
plt.plot(df_split["split_num"], df_split["fair_num"], marker="o")
plt.xlabel("Tỷ lệ lưu lượng đưa vào liên kết 5 GHz")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Mức độ công bằng theo tỷ lệ phân phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/cong_bang_theo_ty_le_phan_phoi.png")
plt.close()

plt.figure()
plt.plot(df_split["split_num"], df_split["loss_num"], marker="o")
plt.xlabel("Tỷ lệ lưu lượng đưa vào liên kết 5 GHz")
plt.ylabel("Tỷ lệ mất gói (%)")
plt.title("Tỷ lệ mất gói theo tỷ lệ phân phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/mat_goi_theo_ty_le_phan_phoi.png")
plt.close()

# =========================
# 3. QUÉT TẢI ĐẦU VÀO
# =========================
df_load = df[df["scenario"] == "load_sweep"].copy().sort_values("offered_num")

plt.figure()
plt.plot(df_load["offered_num"], df_load["thr_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mbps)")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo tải đầu vào - chế độ điều phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/thong_luong_theo_tai_dau_vao.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["delay_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mbps)")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo tải đầu vào - chế độ điều phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/do_tre_theo_tai_dau_vao.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["eff_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA (Mbps)")
plt.ylabel("Hiệu suất (%)")
plt.title("Hiệu suất theo tải đầu vào - chế độ điều phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/hieu_suat_theo_tai_dau_vao.png")
plt.close()

# =========================
# 4. QUÉT SỐ LƯỢNG STA
# =========================
df_sta = df[df["scenario"] == "sta_scaling"].copy().sort_values("nSta_num")

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["thr_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo số lượng STA - chế độ điều phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/thong_luong_theo_so_luong_sta.png")
plt.close()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["fair_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Mức độ công bằng theo số lượng STA - chế độ điều phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/cong_bang_theo_so_luong_sta.png")
plt.close()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["delay_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo số lượng STA - chế độ điều phối lưu lượng")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo6/do_tre_theo_so_luong_sta.png")
plt.close()

print("DONE! Các biểu đồ Demo 6 đã được lưu trong thư mục plots_demo6/")
print("DONE! File chuẩn hóa đã được lưu: demo6_results_chuan_hoa_tieng_viet.csv")
