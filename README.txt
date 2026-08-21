# Wi-Fi 7 Simulation Framework for ns-3

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22023987.svg)](https://doi.org/10.5281/zenodo.22023987)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with ns-3](https://img.shields.io/badge/Made%20with-ns--3-0077B5)](https://www.nsnam.org/)

---

## Tổng quan

Kho mã nguồn này chứa mã mô phỏng, các tập lệnh tự động hóa, chương trình phân tích và dữ liệu CSV được sử dụng trong đồ án tốt nghiệp thạc sĩ:

> **Đánh giá hiệu năng Multi-Link Operation trong mạng IEEE 802.11be bằng phương pháp mô phỏng**

Mục tiêu của framework là xây dựng một quy trình thực nghiệm có khả năng tái lập để khảo sát hiệu năng của Wi-Fi 7 và mô hình đa liên kết ở cấp độ hệ thống bằng ns-3.

Các chỉ tiêu chính được phân tích gồm:

* Thông lượng;
* Độ trễ;
* Độ biến thiên trễ;
* Tỷ lệ mất gói;
* Hiệu suất sử dụng tải;
* Chỉ số công bằng Jain.

Mô hình trong nghiên cứu sử dụng hai giao diện Wi-Fi độc lập trên các băng tần 5 GHz và 6 GHz. Đây là mô hình gần đúng ở cấp độ hệ thống, không phải hiện thực đầy đủ AP MLD, non-AP MLD, MAC chung và TID-to-Link Mapping theo toàn bộ đặc tả IEEE 802.11be.

---

## Cấu trúc repository

```text
MLO_Thesis/
├── src/
│   ├── prep-env-wifi7-check.cc
│   ├── prep-mlo-capability-check.cc
│   ├── demo-1-single-link-baseline.cc
│   ├── demo-2-dual-link.cc
│   ├── demo-3-multi-sta-single-link.cc
│   ├── demo-4-multi-sta-dual-link.cc
│   ├── demo-5-multiband-evaluation.cc
│   ├── demo-6-traffic-steering.cc
│   └── demo-7-robustness.cc
│
├── bash/
│   ├── run_demo_1.sh
│   ├── run_demo_2.sh
│   ├── run_demo_3.sh
│   ├── run_demo_4.sh
│   ├── run_demo_5.sh
│   ├── run_demo_6.sh
│   └── run_demo_7.sh
│
├── python/
│   ├── demo1_analysis.py
│   ├── demo2_analysis.py
│   ├── demo3_analysis.py
│   ├── demo4_analysis.py
│   ├── demo5_analysis.py
│   ├── demo6_analysis.py
│   └── demo7_analysis.py
│
├── data/
│   ├── demo1_results.csv
│   ├── demo2_results.csv
│   ├── demo3_results.csv
│   ├── demo4_results.csv
│   ├── demo5_results.csv
│   ├── demo6_results.csv
│   └── demo7_results.csv
│
├── CITATION.cff
├── LICENSE
└── README.txt
```

---

## Yêu cầu hệ thống

| Thành phần   | Phiên bản khuyến nghị |
| ------------ | --------------------- |
| ns-3         | 3.46.1 hoặc mới hơn   |
| GNU g++      | 9.0 hoặc mới hơn      |
| Python       | 3.8 hoặc mới hơn      |
| Bash         | 4.0 hoặc mới hơn      |
| Hệ điều hành | Linux, macOS hoặc WSL |

Cài đặt các thư viện Python:

```bash
pip install pandas matplotlib seaborn numpy scipy
```

---

## Chuẩn bị môi trường ns-3

Sao chép mã nguồn mô phỏng vào thư mục `scratch` của ns-3:

```bash
cp src/*.cc /path/to/ns-3.46.1/scratch/
```

Biên dịch ns-3:

```bash
cd /path/to/ns-3.46.1
./ns3 configure
./ns3 build
```

---

## Chạy các Demo

Các tập lệnh Bash sử dụng lệnh `./ns3`, vì vậy nên chạy chúng từ thư mục gốc của ns-3:

```bash
cd /path/to/ns-3.46.1
```

Cấp quyền thực thi:

```bash
chmod +x /path/to/MLO_Thesis/bash/run_demo_*.sh
```

Chạy từng Demo:

```bash
bash /path/to/MLO_Thesis/bash/run_demo_1.sh
bash /path/to/MLO_Thesis/bash/run_demo_2.sh
bash /path/to/MLO_Thesis/bash/run_demo_3.sh
bash /path/to/MLO_Thesis/bash/run_demo_4.sh
bash /path/to/MLO_Thesis/bash/run_demo_5.sh
bash /path/to/MLO_Thesis/bash/run_demo_6.sh
bash /path/to/MLO_Thesis/bash/run_demo_7.sh
```

Các tệp CSV được sinh ra trong thư mục hiện hành của ns-3. Có thể sao chép chúng về thư mục dữ liệu của repository:

```bash
cp demo1_results.csv /path/to/MLO_Thesis/data/
cp demo2_results.csv /path/to/MLO_Thesis/data/
cp demo3_results.csv /path/to/MLO_Thesis/data/
cp demo4_results.csv /path/to/MLO_Thesis/data/
cp demo5_results.csv /path/to/MLO_Thesis/data/
cp demo6_results.csv /path/to/MLO_Thesis/data/
cp demo7_results.csv /path/to/MLO_Thesis/data/
```

---

## Phạm vi các Demo

| Demo   | Nội dung                                | Số lượt chạy |
| ------ | --------------------------------------- | -----------: |
| Demo 1 | Baseline đơn liên kết                   |           41 |
| Demo 2 | Dual-link trên 5 GHz và 6 GHz           |           51 |
| Demo 3 | Nhiều STA, đơn liên kết                 |           46 |
| Demo 4 | Nhiều STA, dual-link                    |           43 |
| Demo 5 | Đánh giá đa băng tần và độ rộng kênh    |           37 |
| Demo 6 | Phân phối lưu lượng giữa các liên kết   |           25 |
| Demo 7 | Đánh giá trong điều kiện không lý tưởng |          112 |

Tổng cộng có:

```text
41 + 51 + 46 + 43 + 37 + 25 + 112 = 355 lượt chạy
```

Trong toàn bộ các Demo, MCS được cố định ở mức 7. Demo 7 được phân tích như một nhóm tham chiếu riêng vì sử dụng các điều kiện fading, tính di động, tải đầu vào và `RngRun` khác với nhóm thí nghiệm cơ sở.

---

## Cấu trúc dữ liệu CSV

Các Demo không sử dụng cùng một schema CSV. Header của từng tệp như sau:

```text
demo1_results.csv
scenario,nSta,offeredPerSta,totalOffered,throughput,loss,delayMs,jitterMs,efficiency,fairness
```

```text
demo2_results.csv
scenario,nSta,totalOffered,thr5,thr6,total,loss,delayMs,jitterMs,efficiency,fairness
```

```text
demo3_results.csv
scenario,nSta,offeredPerSta,totalOffered,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
```

```text
demo4_results.csv
scenario,nSta,offeredPerStaPerLink,totalOffered,thr5,thr6,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
```

```text
demo5_results.csv
scenario,mode,band,nSta,offeredPerSta,totalOffered,width,mcs,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
```

```text
demo6_results.csv
scenario,mode,split,nSta,offeredPerSta,totalOffered,thr5,thr6,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
```

```text
demo7_results.csv
scenario,nSta,mode,speed,m,offeredPerSta,totalOffered,thrTotal,loss,delayMs,jitterMs,efficiency,fairness
```

Ý nghĩa một số trường thường gặp:

| Trường                 | Ý nghĩa                                     | Đơn vị           |
| ---------------------- | ------------------------------------------- | ---------------- |
| `nSta`                 | Số lượng trạm                               | STA              |
| `offeredPerSta`        | Tải cung cấp trên mỗi STA                   | Mbps             |
| `offeredPerStaPerLink` | Tải cung cấp trên mỗi STA trên mỗi liên kết | Mbps             |
| `totalOffered`         | Tổng tải cung cấp của kịch bản              | Mbps             |
| `thr5`                 | Thông lượng trên liên kết 5 GHz             | Mbps             |
| `thr6`                 | Thông lượng trên liên kết 6 GHz             | Mbps             |
| `total`, `thrTotal`    | Thông lượng tổng                            | Mbps             |
| `loss`                 | Tỷ lệ mất gói                               | %                |
| `delayMs`              | Độ trễ trung bình                           | ms               |
| `jitterMs`             | Độ biến thiên trễ                           | ms               |
| `efficiency`           | Hiệu suất sử dụng tải cung cấp              | %                |
| `fairness`             | Chỉ số công bằng Jain                       | Không thứ nguyên |
| `width`                | Độ rộng kênh                                | MHz              |
| `mcs`                  | Chỉ số điều chế và mã hóa                   | —                |
| `speed`                | Tốc độ di chuyển                            | m/s              |
| `m`                    | Tham số fading Nakagami                     | —                |
| `RngRun`               | Lần chạy ngẫu nhiên                         | —                |

---

## Phân tích và trực quan hóa

Các chương trình Python nhận đường dẫn CSV đầu vào tùy chọn. Ví dụ:

```bash
cd /path/to/MLO_Thesis/python
python3 demo1_analysis.py ../data/demo1_results.csv
python3 demo2_analysis.py ../data/demo2_results.csv
python3 demo3_analysis.py ../data/demo3_results.csv
python3 demo4_analysis.py ../data/demo4_results.csv
python3 demo5_analysis.py ../data/demo5_results.csv
python3 demo6_analysis.py ../data/demo6_results.csv
python3 demo7_analysis.py ../data/demo7_results.csv
```

Mỗi chương trình tạo các biểu đồ trong thư mục tương ứng:

```text
plots_demo1/
plots_demo2/
plots_demo3/
plots_demo4/
plots_demo5/
plots_demo6/
plots_demo7/
```

---

## Khả năng tái lập

Các kết quả trong repository được tạo theo quy trình:

```text
Mã nguồn ns-3
      ↓
Tập lệnh Bash tự động hóa
      ↓
Tệp CSV kết quả
      ↓
Chương trình Python phân tích
      ↓
Biểu đồ và số liệu tổng hợp
```

Các kịch bản Demo 1–6 sử dụng `RngRun = 1`. Demo 7 được chạy lặp lại với các giá trị `RngRun` từ 1 đến 5 để quan sát độ biến thiên của kết quả.

Mô hình dual-link sử dụng hai `WifiNetDevice` độc lập trên băng tần 5 GHz và 6 GHz. Mô hình này phục vụ đánh giá xu hướng hiệu năng ở cấp độ hệ thống và không được dùng để khẳng định tính tuân thủ đầy đủ của một thiết bị MLO theo chuẩn IEEE 802.11be.

---

## DOI và trích dẫn

DOI tổng hợp của repository:

```text
https://doi.org/10.5281/zenodo.22023987
```

DOI của phiên bản hiện tại `v1.1.1`:

```text
https://doi.org/10.5281/zenodo.22037398
```

BibTeX:

```bibtex
@software{ho_duc_dung_2026_wifi7,
  author = {Hồ, Đức Dũng},
  title = {Wi-Fi 7 Simulation Framework for ns-3},
  year = {2026},
  publisher = {Zenodo},
  version = {v1.1.1},
  doi = {10.5281/zenodo.22037398},
  url = {https://github.com/ducdungpk/MLO_Thesis}
}
```

---

## Giấy phép

Dự án được phân phối theo giấy phép MIT. Xem tệp `LICENSE` để biết thêm chi tiết.

---

## Thông tin tác giả

**Tác giả:** Hồ Đức Dũng
**Email:** [ducdung.pk@gmail.com](mailto:ducdung.pk@gmail.com)
**Cơ sở đào tạo:** Đại học Duy Tân
**Giảng viên hướng dẫn:** TS. Võ Nhân Văn

---

## Tài liệu tham khảo chính

Framework được xây dựng dựa trên tài liệu IEEE 802.11be, tài liệu ns-3 và các nghiên cứu liên quan đến Multi-Link Operation, traffic steering, WLAN performance, fairness và wireless channel modeling.

Danh mục tài liệu tham khảo đầy đủ được trình bày trong luận văn và các tài liệu trích dẫn đi kèm repository.
