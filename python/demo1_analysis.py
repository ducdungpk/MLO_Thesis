import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# DEMO 1 - PHÂN TÍCH KẾT QUẢ
# Dùng cho CSV mới:
# scenario,nSta,offeredPerSta,totalOffered,throughput,loss,delayMs,jitterMs,efficiency,fairness
# Vẫn hỗ trợ CSV cũ có dạng key=value để tránh lỗi khi đọc lại file cũ.
# =========================

PLOTS_DIR = "plots_demo1"


def ensure_dir(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)


def extract_number(series: pd.Series) -> pd.Series:
    """Lấy phần số từ cả dạng sạch '10' và dạng cũ 'offeredPerSta=10'."""
    return pd.to_numeric(
        series.astype(str).str.extract(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)")[0],
        errors="coerce",
    )


def pick_input_file() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    if os.path.exists("demo1_results.csv"):
        return "demo1_results.csv"
    if os.path.exists("demo1_results(1).csv"):
        return "demo1_results(1).csv"
    raise FileNotFoundError(
        "Không tìm thấy file demo1_results.csv. Có thể truyền đường dẫn: "
        "python demo1_analysis_output-fixed.py <duong_dan_csv>"
    )


def save_line_plot(data: pd.DataFrame, x_col: str, y_col: str, xlabel: str, ylabel: str,
                   title: str, output_name: str) -> None:
    if data.empty:
        print(f"Bỏ qua biểu đồ '{title}' vì không có dữ liệu.")
        return

    plot_data = data[[x_col, y_col]].dropna().sort_values(x_col)
    if plot_data.empty:
        print(f"Bỏ qua biểu đồ '{title}' vì dữ liệu không hợp lệ.")
        return

    plt.figure(figsize=(8, 5))
    plt.plot(plot_data[x_col], plot_data[y_col], marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, output_name), dpi=300)
    plt.close()


# Font mặc định của matplotlib thường hỗ trợ tiếng Việt tốt; dòng này giúp ổn định hơn.
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

input_file = pick_input_file()
df = pd.read_csv(input_file)
df.columns = [c.strip() for c in df.columns]

print("File đầu vào:", input_file)
print("Các cột tìm thấy:", list(df.columns))

required_cols = {"scenario", "nSta", "throughput", "loss", "delayMs", "jitterMs", "efficiency", "fairness"}
missing_cols = required_cols - set(df.columns)
if missing_cols:
    raise KeyError(f"Thiếu cột bắt buộc: {sorted(missing_cols)}. Các cột hiện có: {list(df.columns)}")

# CSV mới dùng offeredPerSta; CSV cũ có thể dùng offered.
if "offeredPerSta" in df.columns:
    offered_col = "offeredPerSta"
elif "offered" in df.columns:
    offered_col = "offered"
else:
    raise KeyError(f"Không tìm thấy cột offeredPerSta/offered. Các cột hiện có: {list(df.columns)}")

# totalOffered có trong CSV mới. Nếu đọc CSV cũ không có, tính lại từ nSta * offeredPerSta.
df["scenario"] = df["scenario"].astype(str).str.strip()
df["nSta_num"] = extract_number(df["nSta"])
df["offeredPerSta_num"] = extract_number(df[offered_col])

if "totalOffered" in df.columns:
    df["totalOffered_num"] = extract_number(df["totalOffered"])
else:
    df["totalOffered_num"] = df["nSta_num"] * df["offeredPerSta_num"]

df["throughput_num"] = extract_number(df["throughput"])
df["loss_num"] = extract_number(df["loss"])
df["delay_num"] = extract_number(df["delayMs"])
df["jitter_num"] = extract_number(df["jitterMs"])
df["efficiency_num"] = extract_number(df["efficiency"])
df["fairness_num"] = extract_number(df["fairness"])

print("Các kịch bản:", df["scenario"].unique())

load_sweep = df[df["scenario"] == "single_sta_load_sweep"].copy()
sta_scaling = df[df["scenario"] == "multi_sta_scaling"].copy()
stress_test = df[df["scenario"] == "stress_test"].copy()

print("Số dòng kịch bản quét tải 1 STA:", len(load_sweep))
print("Số dòng kịch bản mở rộng số STA:", len(sta_scaling))
print("Số dòng kịch bản tải nặng:", len(stress_test))

ensure_dir(PLOTS_DIR)

# 1) Quét tải với 1 STA
save_line_plot(
    load_sweep,
    "offeredPerSta_num",
    "throughput_num",
    "Tải đầu vào mỗi STA (Mbps)",
    "Thông lượng (Mbps)",
    "Thông lượng theo tải đầu vào - đơn liên kết, 1 STA",
    "demo1_thong_luong_theo_tai.png",
)

save_line_plot(
    load_sweep,
    "offeredPerSta_num",
    "delay_num",
    "Tải đầu vào mỗi STA (Mbps)",
    "Độ trễ trung bình (ms)",
    "Độ trễ theo tải đầu vào - đơn liên kết, 1 STA",
    "demo1_do_tre_theo_tai.png",
)

save_line_plot(
    load_sweep,
    "offeredPerSta_num",
    "loss_num",
    "Tải đầu vào mỗi STA (Mbps)",
    "Tỷ lệ mất gói (%)",
    "Tỷ lệ mất gói theo tải đầu vào - đơn liên kết, 1 STA",
    "demo1_mat_goi_theo_tai.png",
)

save_line_plot(
    load_sweep,
    "offeredPerSta_num",
    "efficiency_num",
    "Tải đầu vào mỗi STA (Mbps)",
    "Hiệu suất (%)",
    "Hiệu suất theo tải đầu vào - đơn liên kết, 1 STA",
    "demo1_hieu_suat_theo_tai.png",
)

# 2) Mở rộng theo số STA
save_line_plot(
    sta_scaling,
    "nSta_num",
    "throughput_num",
    "Số lượng STA",
    "Thông lượng tổng (Mbps)",
    "Thông lượng theo số lượng STA - đơn liên kết",
    "demo1_thong_luong_theo_so_sta.png",
)

save_line_plot(
    sta_scaling,
    "nSta_num",
    "fairness_num",
    "Số lượng STA",
    "Chỉ số công bằng Jain",
    "Mức độ công bằng theo số lượng STA - đơn liên kết",
    "demo1_cong_bang_theo_so_sta.png",
)

# 3) Xuất thêm dữ liệu đã chuẩn hóa để kiểm tra nhanh nếu cần
summary_cols = [
    "scenario",
    "nSta_num",
    "offeredPerSta_num",
    "totalOffered_num",
    "throughput_num",
    "loss_num",
    "delay_num",
    "jitter_num",
    "efficiency_num",
    "fairness_num",
]
summary = df[summary_cols].rename(columns={
    "scenario": "kich_ban",
    "nSta_num": "so_sta",
    "offeredPerSta_num": "tai_moi_sta_mbps",
    "totalOffered_num": "tong_tai_mbps",
    "throughput_num": "thong_luong_mbps",
    "loss_num": "mat_goi_phan_tram",
    "delay_num": "do_tre_ms",
    "jitter_num": "jitter_ms",
    "efficiency_num": "hieu_suat_phan_tram",
    "fairness_num": "cong_bang_jain",
})
summary.to_csv("demo1_results_chuan_hoa_tieng_viet.csv", index=False, encoding="utf-8-sig")

print(f"HOÀN TẤT. Biểu đồ đã lưu trong thư mục '{PLOTS_DIR}'.")
print("Đã lưu thêm file dữ liệu chuẩn hóa: demo1_results_chuan_hoa_tieng_viet.csv")
