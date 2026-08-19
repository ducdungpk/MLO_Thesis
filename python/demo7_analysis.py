import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def extract_number(series):
    """Trích số từ cả CSV sạch và CSV cũ dạng key=value."""
    return series.astype(str).str.extract(r'([-+]?\d*\.?\d+)')[0].astype(float)

def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def pick_col(df, candidates, label):
    """Chọn cột theo danh sách tên có thể có để tương thích CSV cũ/mới."""
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f"Không tìm thấy cột {label}. Các cột hiện có: {list(df.columns)}")

# Giữ đúng tên file CSV do run_demo_7.sh sinh ra
file = sys.argv[1] if len(sys.argv) > 1 else "demo7_results.csv"

# Đọc file linh hoạt: tự nhận diện dấu phân cách
df = pd.read_csv(file, sep=None, engine="python")

# Chuẩn hóa tên cột
df.columns = [c.strip() for c in df.columns]

print("Columns:", df.columns.tolist())

if "scenario" not in df.columns:
    raise ValueError("Không tìm thấy cột 'scenario'. Hãy kiểm tra lại file input hoặc dấu phân cách.")

df["scenario"] = df["scenario"].astype(str).str.strip()

ensure_dir("plots_demo7")

# =========================
# CHUẨN HÓA THEO CSV MỚI
# Header mới:
# scenario,nSta,mode,speed,m,offeredPerSta,totalOffered,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
# Vẫn hỗ trợ một số tên cũ: load, thr
# =========================
nsta_col = pick_col(df, ["nSta"], "số STA")
mode_col = pick_col(df, ["mode"], "chế độ")
speed_col = pick_col(df, ["speed"], "tốc độ")
m_col = pick_col(df, ["m"], "tham số Nakagami m")
offered_col = pick_col(df, ["offeredPerSta", "load"], "tải đầu vào")
thr_col = pick_col(df, ["thrTotal", "thr"], "thông lượng")
loss_col = pick_col(df, ["loss"], "tỷ lệ mất gói")
delay_col = pick_col(df, ["delayMs"], "độ trễ")
jitter_col = pick_col(df, ["jitterMs"], "jitter")
fair_col = pick_col(df, ["fairness"], "công bằng")

df["so_sta"] = extract_number(df[nsta_col])
df["che_do"] = extract_number(df[mode_col])
df["toc_do"] = extract_number(df[speed_col])
df["nakagami_m"] = extract_number(df[m_col])
df["tai_dau_vao_mbps"] = extract_number(df[offered_col])
df["thong_luong_mbps"] = extract_number(df[thr_col])
df["ty_le_mat_goi_phan_tram"] = extract_number(df[loss_col])
df["do_tre_ms"] = extract_number(df[delay_col])
df["jitter_ms"] = extract_number(df[jitter_col])
df["cong_bang_jain"] = extract_number(df[fair_col])

if "totalOffered" in df.columns:
    df["tong_tai_dau_vao_mbps"] = extract_number(df["totalOffered"])
else:
    df["tong_tai_dau_vao_mbps"] = df["so_sta"] * df["tai_dau_vao_mbps"]

if "efficiency" in df.columns:
    df["hieu_suat_phan_tram"] = extract_number(df["efficiency"])
else:
    df["hieu_suat_phan_tram"] = (df["thong_luong_mbps"] / df["tong_tai_dau_vao_mbps"]) * 100.0

# Xuất thêm file chuẩn hóa tên cột tiếng Việt không dấu để dùng lại khi viết báo cáo
cols_out = [
    "scenario",
    "so_sta",
    "che_do",
    "toc_do",
    "nakagami_m",
    "tai_dau_vao_mbps",
    "tong_tai_dau_vao_mbps",
    "thong_luong_mbps",
    "ty_le_mat_goi_phan_tram",
    "do_tre_ms",
    "jitter_ms",
    "hieu_suat_phan_tram",
    "cong_bang_jain",
]
df[cols_out].to_csv("demo7_results_chuan_hoa_tieng_viet.csv", index=False)

print("Scenarios:", df["scenario"].unique())

# =========================
# 1. ĐỘ ỔN ĐỊNH QUA CÁC LẦN CHẠY LẶP
# =========================
df_rep = df[df["scenario"] == "repeat_test"].copy()

if not df_rep.empty:
    plt.figure()
    plt.plot(range(1, len(df_rep) + 1), df_rep["thong_luong_mbps"], marker="o")
    plt.xlabel("Lần chạy")
    plt.ylabel("Thông lượng (Mb/s)")
    plt.title("Biến thiên thông lượng qua các lần chạy lặp lại")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/bien_thien_thong_luong_lap_lai.png")
    plt.close()

# =========================
# 2. ẢNH HƯỞNG CỦA DI CHUYỂN
# =========================
df_mob = df[df["scenario"] == "mobility_sweep"].copy().sort_values("toc_do")

if not df_mob.empty:
    plt.figure()
    plt.plot(df_mob["toc_do"], df_mob["thong_luong_mbps"], marker="o")
    plt.xlabel("Tốc độ di chuyển (m/s)")
    plt.ylabel("Thông lượng (Mb/s)")
    plt.title("Thông lượng theo tốc độ di chuyển")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/thong_luong_theo_toc_do_di_chuyen.png")
    plt.close()

    plt.figure()
    plt.plot(df_mob["toc_do"], df_mob["do_tre_ms"], marker="o")
    plt.xlabel("Tốc độ di chuyển (m/s)")
    plt.ylabel("Độ trễ (ms)")
    plt.title("Độ trễ theo tốc độ di chuyển")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/do_tre_theo_toc_do_di_chuyen.png")
    plt.close()

    plt.figure()
    plt.plot(df_mob["toc_do"], df_mob["ty_le_mat_goi_phan_tram"], marker="o")
    plt.xlabel("Tốc độ di chuyển (m/s)")
    plt.ylabel("Tỷ lệ mất gói (%)")
    plt.title("Tỷ lệ mất gói theo tốc độ di chuyển")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/mat_goi_theo_toc_do_di_chuyen.png")
    plt.close()

# =========================
# 3. ẢNH HƯỞNG CỦA FADING
# =========================
df_fade = df[df["scenario"] == "fading_sweep"].copy().sort_values("nakagami_m")

if not df_fade.empty:
    plt.figure()
    plt.plot(df_fade["nakagami_m"], df_fade["thong_luong_mbps"], marker="o")
    plt.xlabel("Tham số Nakagami m")
    plt.ylabel("Thông lượng (Mb/s)")
    plt.title("Thông lượng theo tham số fading")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/thong_luong_theo_fading.png")
    plt.close()

    plt.figure()
    plt.plot(df_fade["nakagami_m"], df_fade["do_tre_ms"], marker="o")
    plt.xlabel("Tham số Nakagami m")
    plt.ylabel("Độ trễ (ms)")
    plt.title("Độ trễ theo tham số fading")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/do_tre_theo_fading.png")
    plt.close()

# =========================
# 4. ẢNH HƯỞNG CỦA TẢI ĐẦU VÀO
# =========================
df_load = df[df["scenario"] == "load_sweep"].copy().sort_values("tai_dau_vao_mbps")

if not df_load.empty:
    plt.figure()
    plt.plot(df_load["tai_dau_vao_mbps"], df_load["thong_luong_mbps"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
    plt.ylabel("Thông lượng (Mb/s)")
    plt.title("Thông lượng theo tải đầu vào trong điều kiện không lý tưởng")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/thong_luong_theo_tai_dau_vao.png")
    plt.close()

    plt.figure()
    plt.plot(df_load["tai_dau_vao_mbps"], df_load["do_tre_ms"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
    plt.ylabel("Độ trễ (ms)")
    plt.title("Độ trễ theo tải đầu vào trong điều kiện không lý tưởng")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/do_tre_theo_tai_dau_vao.png")
    plt.close()

    plt.figure()
    plt.plot(df_load["tai_dau_vao_mbps"], df_load["ty_le_mat_goi_phan_tram"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
    plt.ylabel("Tỷ lệ mất gói (%)")
    plt.title("Tỷ lệ mất gói theo tải đầu vào trong điều kiện không lý tưởng")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/mat_goi_theo_tai_dau_vao.png")
    plt.close()

# =========================
# 5. STRESS TEST: TỔNG HỢP THEO TẢI ĐẦU VÀO
# =========================
df_stress = df[df["scenario"] == "stress_test"].copy()

if not df_stress.empty:
    stress_mean = (
        df_stress
        .groupby("tai_dau_vao_mbps", as_index=False)[["thong_luong_mbps", "do_tre_ms", "ty_le_mat_goi_phan_tram"]]
        .mean()
        .sort_values("tai_dau_vao_mbps")
    )

    plt.figure()
    plt.plot(stress_mean["tai_dau_vao_mbps"], stress_mean["thong_luong_mbps"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
    plt.ylabel("Thông lượng trung bình (Mb/s)")
    plt.title("Thông lượng trung bình trong kịch bản stress test")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/thong_luong_trung_binh_stress_test.png")
    plt.close()

    plt.figure()
    plt.plot(stress_mean["tai_dau_vao_mbps"], stress_mean["do_tre_ms"], marker="o")
    plt.xlabel("Tải đầu vào mỗi STA (Mb/s)")
    plt.ylabel("Độ trễ trung bình (ms)")
    plt.title("Độ trễ trung bình trong kịch bản stress test")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots_demo7/do_tre_trung_binh_stress_test.png")
    plt.close()

print("DONE! Biểu đồ Demo 7 đã lưu trong thư mục 'plots_demo7'.")
print("File dữ liệu chuẩn hóa: demo7_results_chuan_hoa_tieng_viet.csv")
