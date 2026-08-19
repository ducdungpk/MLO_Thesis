import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def extract_number(series):
    """Lấy phần số từ cột, hỗ trợ cả CSV sạch và CSV cũ dạng key=value."""
    return series.astype(str).str.extract(r'([-+]?\d*\.?\d+)')[0].astype(float)


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


# ===== LOAD DATA =====
# Giữ đúng tên file CSV cũ do run_demo_4.sh sinh ra.
file = sys.argv[1] if len(sys.argv) > 1 else "demo4_results.csv"

df = pd.read_csv(file, sep=None, engine="python")
df.columns = [c.strip() for c in df.columns]
df["scenario"] = df["scenario"].astype(str).str.strip()

print("Các cột đọc được:", df.columns.tolist())
print("Các kịch bản:", df["scenario"].unique())

ensure_dir("plots_demo4")

# ===== KIỂM TRA CỘT THEO FORMAT CSV MỚI =====
required_cols = [
    "scenario",
    "nSta",
    "offeredPerStaPerLink",
    "totalOffered",
    "thr5",
    "thr6",
    "thrTotal",
    "loss",
    "delayMs",
    "jitterMs",
    "efficiency",
    "fairness",
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise KeyError(
        "Thiếu cột trong demo4_results.csv: "
        + ", ".join(missing)
        + f". Các cột hiện có: {list(df.columns)}"
    )

# ===== CHUẨN HÓA SỐ LIỆU =====
df["nSta_num"] = extract_number(df["nSta"])
df["offered_num"] = extract_number(df["offeredPerStaPerLink"])
df["total_offered_num"] = extract_number(df["totalOffered"])
df["thr5_num"] = extract_number(df["thr5"])
df["thr6_num"] = extract_number(df["thr6"])
df["thr_num"] = extract_number(df["thrTotal"])
df["loss_num"] = extract_number(df["loss"])            # CSV mới đã là %
df["delay_num"] = extract_number(df["delayMs"])
df["jitter_num"] = extract_number(df["jitterMs"])
df["eff_num"] = extract_number(df["efficiency"])       # CSV mới đã là %
df["fair_num"] = extract_number(df["fairness"])

# ===== XUẤT FILE DỮ LIỆU CHUẨN HÓA VỚI TÊN CỘT TIẾNG VIỆT =====
df_vn = pd.DataFrame({
    "Kịch bản": df["scenario"],
    "Số lượng STA": df["nSta_num"],
    "Tải mỗi STA mỗi liên kết (Mbps)": df["offered_num"],
    "Tổng tải đầu vào (Mbps)": df["total_offered_num"],
    "Thông lượng 5 GHz (Mbps)": df["thr5_num"],
    "Thông lượng 6 GHz (Mbps)": df["thr6_num"],
    "Tổng thông lượng (Mbps)": df["thr_num"],
    "Tỷ lệ mất gói (%)": df["loss_num"],
    "Độ trễ (ms)": df["delay_num"],
    "Jitter (ms)": df["jitter_num"],
    "Hiệu suất (%)": df["eff_num"],
    "Chỉ số công bằng Jain": df["fair_num"],
})
df_vn.to_csv("demo4_results_chuan_hoa_tieng_viet.csv", index=False, encoding="utf-8-sig")

# =========================
# LOAD SWEEP
# =========================
df_load = df[df["scenario"] == "load_sweep"].copy()

plt.figure()
plt.plot(df_load["offered_num"], df_load["thr_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA trên mỗi liên kết (Mbps)")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo tải đầu vào - đa liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/thong_luong_theo_tai_dau_vao.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["thr5_num"], marker="o", label="5 GHz")
plt.plot(df_load["offered_num"], df_load["thr6_num"], marker="o", label="6 GHz")
plt.xlabel("Tải đầu vào mỗi STA trên mỗi liên kết (Mbps)")
plt.ylabel("Thông lượng từng liên kết (Mbps)")
plt.title("Phân bố thông lượng trên hai liên kết theo tải đầu vào")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/thong_luong_tung_lien_ket_theo_tai.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["delay_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA trên mỗi liên kết (Mbps)")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo tải đầu vào - đa liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/do_tre_theo_tai_dau_vao.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["loss_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA trên mỗi liên kết (Mbps)")
plt.ylabel("Tỷ lệ mất gói (%)")
plt.title("Tỷ lệ mất gói theo tải đầu vào - đa liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/ty_le_mat_goi_theo_tai_dau_vao.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["fair_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA trên mỗi liên kết (Mbps)")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Công bằng theo tải đầu vào - đa liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/cong_bang_theo_tai_dau_vao.png")
plt.close()

plt.figure()
plt.plot(df_load["offered_num"], df_load["eff_num"], marker="o")
plt.xlabel("Tải đầu vào mỗi STA trên mỗi liên kết (Mbps)")
plt.ylabel("Hiệu suất (%)")
plt.title("Hiệu suất theo tải đầu vào - đa liên kết, nhiều STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/hieu_suat_theo_tai_dau_vao.png")
plt.close()

# =========================
# STA SCALING
# =========================
df_sta = df[df["scenario"] == "sta_scaling"].copy()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["thr_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo số lượng STA - đa liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/thong_luong_theo_so_luong_sta.png")
plt.close()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["thr5_num"], marker="o", label="5 GHz")
plt.plot(df_sta["nSta_num"], df_sta["thr6_num"], marker="o", label="6 GHz")
plt.xlabel("Số lượng STA")
plt.ylabel("Thông lượng từng liên kết (Mbps)")
plt.title("Phân bố thông lượng trên hai liên kết theo số lượng STA")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/thong_luong_tung_lien_ket_theo_so_luong_sta.png")
plt.close()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["fair_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Công bằng theo số lượng STA - đa liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/cong_bang_theo_so_luong_sta.png")
plt.close()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["delay_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo số lượng STA - đa liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/do_tre_theo_so_luong_sta.png")
plt.close()

plt.figure()
plt.plot(df_sta["nSta_num"], df_sta["eff_num"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Hiệu suất (%)")
plt.title("Hiệu suất theo số lượng STA - đa liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo4/hieu_suat_theo_so_luong_sta.png")
plt.close()

print("HOÀN TẤT! Biểu đồ Demo 4 đã lưu trong thư mục 'plots_demo4'.")
print("Đã xuất dữ liệu chuẩn hóa: demo4_results_chuan_hoa_tieng_viet.csv")
