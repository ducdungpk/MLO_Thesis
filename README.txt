# Wi-Fi 7 Simulation Framework for ns-3

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with ns-3](https://img.shields.io/badge/Made%20with-ns--3-0077B5)](https://www.nsnam.org/)

---

## Tổng quan

Kho lưu trữ này chứa toàn bộ mã nguồn, kịch bản tự động hóa, và dữ liệu thô được sử dụng trong luận văn thạc sĩ:

> **"Đánh giá hiệu năng cơ chế Multi-Link Operation trong mạng IEEE 802.11be bằng phương pháp mô phỏng"**

###Mục tiêu nghiên cứu

- Triển khai mô phỏng mạng Wi-Fi 7 (802.11be) trên ns-3
- Đánh giá các chỉ số: Throughput, PDR, Delay, Jitter
- Phân tích ảnh hưởng của số nút, tốc độ, tải, SNR
- Đánh giá MLO (Multi-Link Operation)
- So sánh Wi-Fi 6 vs Wi-Fi 7

---

##Cấu trúc thư mục
wifi7-simulation-framework/
├── src/ # 9 file ns-3 (.cc)
├── bash/ # 7 bash scripts (.sh)
├── python/ # 7 python scripts (.py)
├── data/ # 7 CSV files
├── LICENSE
├── CITATION.cff
└── README.md

### Chi tiết:

**src/** - Mã nguồn mô phỏng ns-3 (9 files)
- `prep-env-wifi7-check.cc`
- `prep-mlo-capability-check.cc`
- `demo-1-single-link-baseline.cc` 
- `demo-2-dual-link.cc` 
- `demo-3-multi-sta-single-link.cc`
- `demo-4-multi-sta-dual-link.cc` 
- `demo-5-multiband-evaluation.cc` 
- `demo-6-traffic-steering.cc`
- `demo-7-robustness.cc` 
 
**bash/** - Bash scripts tự động hóa (7 files)
- `run_demo_1.sh`
- `run_demo_2.sh`
- `run_demo_3.sh`
- `run_demo_4.sh`
- `run_demo_5.sh`
- `run_demo_6.sh`
- `run_demo_7.sh`

**python/** - Xử lý dữ liệu và vẽ biểu đồ (7 files)
- `demo1_analysis.py` 
- `demo2_analysis.py` 
- `demo3_analysis.py` 
- `demo4_analysis.py` 
- `demo5_analysis.py` 
- `demo6_analysis.py` 
- `demo7_analysis.py` 

**data/** - Dữ liệu thô (7 CSV files)
- `demo1_results.csv`
- `demo2_results.csv`
- `demo3_results.csv`
- `demo4_results.csv`
- `demo5_results.csv`
- `demo6_results.csv`
- `demo7_results.csv`

---

## Yêu cầu hệ thống

| Phần mềm   	| Phiên bản | Ghi chú 									|
|---------------|-----------|-------------------------------------------|
| ns-3 			| 3.46.1+  	| Cần module wifi, applications, internet 	|
| g++ 			| 9.0+ 		| Trình biên dịch C++ 						|
| Python		| 3.8+ 		| Cài pip packages 							|
| Bash 			| 4.0+	 	| Linux/macOS/WSL 							|

### Python packages:
```bash
pip install pandas matplotlib seaborn numpy scipy

Hướng dẫn chạy mô phỏng
1. Clone repository
git clone https://github.com/ducdungpk/MLO_Thesis.git
cd MLO_Thesis

2. Copy code vào ns-3
bash
cp src/*.cc /path/to/ns-3.46.1/scratch/

3. Biên dịch ns-3
bash
cd /path/to/ns-3.46.1
./waf configure
./waf build

4. Chạy mô phỏng
bash
cd /path/to/wifi7-simulation-framework/bash
chmod +x *.sh
./run_demo_1.sh          # Chạy kịch bản 1
./run_demo_2.sh          # Chạy kịch bản 2
./run_demo_3.sh          # Chạy kịch bản 3
./run_demo_4.sh          # Chạy kịch bản 4
./run_demo_5.sh          # Chạy kịch bản 5
./run_demo_6.sh          # Chạy kịch bản 6
./run_demo_7.sh          # Chạy kịch bản 7

5. Xử lý dữ liệu
bash
cd ../python
python3 merge_results.py
python3 statistics.py
python3 plot_throughput.py
python3 plot_pdr_delay.py
python3 plot_heatmap.py
python3 anova_test.py
python3 generate_report.py

Cấu trúc dữ liệu CSV
Cột			Tên				Đơn vị			Mô tả
1			Nodes			-				Số nút mạng
2			Speed			m/s				Tốc độ di chuyển
3			DataRate		Kbps			Tốc độ dữ liệu
4			Throughput		Mbps			Thông lượng
5			PDR				%				Tỷ lệ gói thành công
6			Delay			ms				Độ trễ
7			Jitter			ms				Biến thiên độ trễ
8			SNR (opt)		dB				Tỷ lệ tín/nhiễu
9			Energy (opt)	J				Năng lượng tiêu thụ

Trích dẫn
bibtex
@software{yourname_wifi7_2026,
  author = {[Hồ Đức Dũng]},
  title = {Wi-Fi 7 Simulation Framework for ns-3},
  year = {2026},
  publisher = {Zenodo},
  version = {v1.0.0},
  doi = {10.5281/zenodo.XXXXXXXX},
  url = {https://github.com/ducdung.pk/MLO_Thesis}
}

Giấy phép
Dự án này được phân phối dưới giấy phép MIT License. Xem file LICENSE để biết chi tiết.

Liên hệ
Tác giả: Hồ Đức Dũng
Email: ducdung.pk@gmail.com
Trường: DTU
GVHD: TS. Võ Nhân Văn

Lời cảm ơn
TS. Võ Nhân Văn - Giảng viên hướng dẫn
Cộng đồng ns-3 - Tài liệu và hỗ trợ kỹ thuật
Tài liệu tham khảo