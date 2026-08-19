import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def extract_number(series):
    """Trích số từ cột; hỗ trợ cả CSV sạch và dạng key=value cũ."""
    return series.astype(str).str.extract(r'([-+]?\d*\.?\d+)')[0].astype(float)


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_col(df, candidates, required=True):
    """Lấy tên cột đầu tiên tồn tại trong danh sách candidates."""
    for col in candidates:
        if col in df.columns:
            return col
    if required:
        raise KeyError(
            "Không tìm thấy cột phù hợp. Cần một trong các cột: "
            + ", ".join(candidates)
            + f". Các cột hiện có: {list(df.columns)}"
        )
    return None


# ===== LOAD DATA =====
# Mặc định đọc đúng tên CSV cũ do script demo sinh ra.
file = sys.argv[1] if len(sys.argv) > 1 else "demo2_results.csv"
df = pd.read_csv(file, sep=None, engine="python")

# Clean columns
df.columns = [c.strip() for c in df.columns]
df["scenario"] = df["scenario"].astype(str).str.strip()

print("Các cột đọc được:", df.columns.tolist())
print("Các kịch bản:", df["scenario"].unique())

ensure_dir("plots_demo2")

# ===== PARSE DATA =====
nsta_col = get_col(df, ["nSta"])
# CSV mới của Demo 2 dùng totalOffered; CSV cũ có thể dùng offeredPerLink/offered.
offered_col = get_col(df, ["totalOffered", "offeredPerLink", "offered", "offeredLoad"])

thr5_col = get_col(df, ["thr5"])
thr6_col = get_col(df, ["thr6"])
total_col = get_col(df, ["total", "thrTotal", "throughput"])
delay_col = get_col(df, ["delayMs"])
loss_col = get_col(df, ["loss"])
eff_col = get_col(df, ["efficiency"])
fair_col = get_col(df, ["fairness"])

df["so_sta"] = extract_number(df[nsta_col])
df["tai_dau_vao_mbps"] = extract_number(df[offered_col])
df["thong_luong_5ghz_mbps"] = extract_number(df[thr5_col])
df["thong_luong_6ghz_mbps"] = extract_number(df[thr6_col])
df["tong_thong_luong_mbps"] = extract_number(df[total_col])
df["do_tre_ms"] = extract_number(df[delay_col])
df["ty_le_mat_goi_phan_tram"] = extract_number(df[loss_col])
df["hieu_suat_phan_tram"] = extract_number(df[eff_col])
df["chi_so_cong_bang"] = extract_number(df[fair_col])

# Xuất thêm file chuẩn hóa với tên cột tiếng Việt không dấu để dễ đưa vào báo cáo.
df_vn = df[
    [
        "scenario",
        "so_sta",
        "tai_dau_vao_mbps",
        "thong_luong_5ghz_mbps",
        "thong_luong_6ghz_mbps",
        "tong_thong_luong_mbps",
        "ty_le_mat_goi_phan_tram",
        "do_tre_ms",
        "hieu_suat_phan_tram",
        "chi_so_cong_bang",
    ]
].copy()

df_vn = df_vn.rename(
    columns={
        "scenario": "kich_ban",
        "so_sta": "so_luong_sta",
        "tai_dau_vao_mbps": "tai_dau_vao_mbps",
        "thong_luong_5ghz_mbps": "thong_luong_5ghz_mbps",
        "thong_luong_6ghz_mbps": "thong_luong_6ghz_mbps",
        "tong_thong_luong_mbps": "tong_thong_luong_mbps",
        "ty_le_mat_goi_phan_tram": "ty_le_mat_goi_phan_tram",
        "do_tre_ms": "do_tre_ms",
        "hieu_suat_phan_tram": "hieu_suat_phan_tram",
        "chi_so_cong_bang": "chi_so_cong_bang",
    }
)

df_vn.to_csv("demo2_results_chuan_hoa_tieng_viet.csv", index=False)

# ===== FILTER SCENARIOS =====
df_load = df[df["scenario"] == "load_sweep"].copy()
df_sta = df[df["scenario"] == "sta_scaling"].copy()

print("Số dòng kịch bản quét tải:", len(df_load))
print("Số dòng kịch bản quét số STA:", len(df_sta))

# =========================
# 1) Thông lượng theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_dau_vao_mbps"], df_load["tong_thong_luong_mbps"], marker="o")
plt.xlabel("Tải đầu vào tổng (Mbps)")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo tải đầu vào - đa liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_thong_luong_theo_tai.png")
plt.close()

# =========================
# 2) Thông lượng từng liên kết
# =========================
plt.figure()
plt.plot(df_load["tai_dau_vao_mbps"], df_load["thong_luong_5ghz_mbps"], marker="o", label="Liên kết 5 GHz")
plt.plot(df_load["tai_dau_vao_mbps"], df_load["thong_luong_6ghz_mbps"], marker="o", label="Liên kết 6 GHz")
plt.xlabel("Tải đầu vào tổng (Mbps)")
plt.ylabel("Thông lượng từng liên kết (Mbps)")
plt.title("Phân bố thông lượng trên hai liên kết")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_thong_luong_tung_lien_ket.png")
plt.close()

# =========================
# 3) Hiệu suất theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_dau_vao_mbps"], df_load["hieu_suat_phan_tram"], marker="o")
plt.xlabel("Tải đầu vào tổng (Mbps)")
plt.ylabel("Hiệu suất (%)")
plt.title("Hiệu suất theo tải đầu vào")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_hieu_suat_theo_tai.png")
plt.close()

# =========================
# 4) Độ trễ theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_dau_vao_mbps"], df_load["do_tre_ms"], marker="o")
plt.xlabel("Tải đầu vào tổng (Mbps)")
plt.ylabel("Độ trễ trung bình (ms)")
plt.title("Độ trễ theo tải đầu vào")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_do_tre_theo_tai.png")
plt.close()

# =========================
# 5) Thông lượng theo số lượng STA
# =========================
plt.figure()
plt.plot(df_sta["so_sta"], df_sta["tong_thong_luong_mbps"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Tổng thông lượng (Mbps)")
plt.title("Thông lượng theo số lượng STA - đa liên kết")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_thong_luong_theo_sta.png")
plt.close()

# =========================
# 6) Công bằng theo số lượng STA
# =========================
plt.figure()
plt.plot(df_sta["so_sta"], df_sta["chi_so_cong_bang"], marker="o")
plt.xlabel("Số lượng STA")
plt.ylabel("Chỉ số công bằng Jain")
plt.title("Công bằng theo số lượng STA")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_cong_bang_theo_sta.png")
plt.close()

# =========================
# 7) Tỷ lệ mất gói theo tải đầu vào
# =========================
plt.figure()
plt.plot(df_load["tai_dau_vao_mbps"], df_load["ty_le_mat_goi_phan_tram"], marker="o")
plt.xlabel("Tải đầu vào tổng (Mbps)")
plt.ylabel("Tỷ lệ mất gói (%)")
plt.title("Tỷ lệ mất gói theo tải đầu vào")
plt.grid()
plt.tight_layout()
plt.savefig("plots_demo2/demo2_mat_goi_theo_tai.png")
plt.close()

print("HOÀN TẤT! Biểu đồ Demo 2 đã lưu trong thư mục 'plots_demo2'.")
print("File dữ liệu chuẩn hóa đã lưu: demo2_results_chuan_hoa_tieng_viet.csv")
