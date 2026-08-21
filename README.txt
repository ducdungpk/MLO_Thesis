# Wi-Fi 7 Simulation Framework for ns-3

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22023987.svg)](https://doi.org/10.5281/zenodo.22023987)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with ns-3](https://img.shields.io/badge/Made%20with-ns--3-0077B5)](https://www.nsnam.org/)

---

## Tổng quan

Kho lưu trữ này chứa toàn bộ mã nguồn, kịch bản tự động hóa, và dữ liệu thô được sử dụng trong luận văn thạc sĩ:

> **"Đánh giá hiệu năng cơ chế Multi-Link Operation trong mạng IEEE 802.11be bằng phương pháp mô phỏng"**

### Phiên bản và DOI

- Phiên bản hiện tại: `v1.1.0`
- DOI tổng hợp của toàn bộ các phiên bản:
  https://doi.org/10.5281/zenodo.22023987
- DOI riêng của phiên bản `v1.1.1`:
  https://doi.org/10.5281/zenodo.22037398

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
└── README.txt

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

| Phần mềm   	  | Phiên bản | Ghi chú 									                         |
|---------------|-----------|-------------------------------------------|
| ns-3 			      | 3.46.1+  	| Cần module wifi, applications, internet 	 |
| g++ 			       | 9.0+ 		   | Trình biên dịch C++ 						                |
| Python		      | 3.8+ 		   | Cài pip packages 							                  |
| Bash 			      | 4.0+	 	   | Linux/macOS/WSL 							                   |

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
Cột			Tên				       Đơn vị			Mô tả
1			  Nodes			      -				    Số nút mạng
2			  Speed			       m/s				 Tốc độ di chuyển
3			  DataRate		     Kbps			 Tốc độ dữ liệu
4			  Throughput		   Mbps			 Thông lượng
5			  PDR				        %				   Tỷ lệ gói thành công
6			  Delay			       ms				  Độ trễ
7			  Jitter			      ms				  Biến thiên độ trễ
8			  SNR (opt)		    dB				  Tỷ lệ tín/nhiễu
9			  Energy (opt)	  J				   Năng lượng tiêu thụ

Trích dẫn
bibtex
@software{ho_duc_dung_2026_wifi7,
  author = {Hồ, Đức Dũng},
  title = {Wi-Fi 7 Simulation Framework for ns-3},
  year = {2026},
  publisher = {Zenodo},
  version = {v1.1.1},
  doi = {10.5281/zenodo.22037398},
  url = {https://github.com/ducdungpk/MLO_Thesis}
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
[1] 	A. Garcia-Rodriguez, D. Lopez-Perez, L. Galati-Giordano, and G. Geraci, “IEEE 802.11be: Wi-Fi 7 Strikes Back,” IEEE Communications Magazine, vol. 59, no. 4, pp. 102–108, Apr. 2021, doi: 10.1109/MCOM.001.2000711. 
[2] 	E. Khorov, A. Kiryanov, A. Lyakhov, and G. Bianchi, “A Tutorial on IEEE 802.11ax High Efficiency WLANs,” IEEE Communications Surveys & Tutorials, vol. 21, no. 1, pp. 197–216, First Quarter 2019, doi: 10.1109/COMST.2018.2871099. 
[3] 	P. Chatzimisios, A. C. Boucouvalas, and V. Vitsas, “IEEE 802.11 Packet Delay—A Finite Retry Limit Analysis,” in Proc. IEEE Global Telecommunications Conference (GLOBECOM), vol. 2, 2003, pp. 950–954, doi: 10.1109/GLOCOM.2003.1258379. 
[4] 	A. Kumar, E. Altman, D. Miorandi, and M. Goyal, “New Insights from a Fixed-Point Analysis of Single Cell IEEE 802.11 WLANs,” IEEE/ACM Transactions on Networking, vol. 15, no. 3, pp. 588–601, Jun. 2007, doi: 10.1109/TNET.2007.893091. 
[5] 	A. Lopez-Raventos and B. Bellalta, “Multi-Link Operation in IEEE 802.11be WLANs,” IEEE Wireless Communications, vol. 29, no. 4, pp. 94–100, Aug. 2022, doi: 10.1109/MWC.006.2100404. 
[6] 	M. Carrascosa-Zamacois, L. Galati-Giordano, A. Jonsson, G. Geraci, and B. Bellalta, “Performance and Coexistence Evaluation of IEEE 802.11be Multi-Link Operation,” in Proc. IEEE Wireless Communications and Networking Conference (WCNC), 2023, pp. 1–6, doi: 10.1109/WCNC55385.2023.10118829. 
[7] 	M. Carrascosa-Zamacois, G. Geraci, E. Knightly, and B. Bellalta, “Wi-Fi Multi-Link Operation: An Experimental Study of Latency and Throughput,” IEEE/ACM Transactions on Networking, vol. 32, no. 1, pp. 308–322, Feb. 2024, doi: 10.1109/TNET.2023.3283154. 
[8] 	A. Lopez-Raventos and B. Bellalta, “Dynamic Traffic Allocation in IEEE 802.11be Multi-Link WLANs,” IEEE Wireless Communications Letters, vol. 11, no. 7, pp. 1404–1408, Jul. 2022, doi: 10.1109/LWC.2022.3171442. 
[9] 	S. Kumar, E. Garcia-Villegas, and D. Camps-Mur, “SLA-MLO: Congestion-Aware SLA-Based Scheduling of Multiple Links in IEEE 802.11be,” in Proc. IEEE Consumer Communications & Networking Conference (CCNC), 2024, pp. 875–880, doi: 10.1109/CCNC51664.2024.10454738. 
[10] 	M. Nakagami, “The m-Distribution—A General Formula of Intensity Distribution of Rapid Fading,” in Statistical Methods in Radio Wave Propagation, W. C. Hoffman, Ed. Oxford, U.K.: Pergamon Press, 1960, pp. 3–36, doi: 10.1016/B978-0-08-009306-2.50005-4. 
[11] 	J. Yoon, M. Liu, and B. D. Noble, “Random Waypoint Considered Harmful,” in Proc. IEEE INFOCOM, vol. 2, 2003, pp. 1312–1321, doi: 10.1109/INFCOM.2003.1208967. 
[12] 	ns-3 Project, “ns-3.46.1,” Oct. 16, 2025. [Online]. Available: https://gitlab.com/nsnam/ns-3-dev/-/tags/ns-3.46.1.
[13] 	D. Akhmetov, R. Arefi, H. Yaghoobi, C. Cordeiro, and D. Cavalcanti, “6 GHz Spectrum Needs for Wi-Fi 7,” IEEE Communications Standards Magazine, vol. 6, no. 1, pp. 5–7, Mar. 2022, doi: 10.1109/MCOMSTD.2022.9762843. 
[14] 	M. Ghoshal, S. B. Krishna, F. Gringoli, J. Widmer, and D. Koutsonikolas, “A First Look at 160 MHz WiFi 6/6E in Action: Performance and Interference Characterization,” in Proc. IFIP Networking Conference, 2024, pp. 489–495, doi: 10.23919/IFIPNETWORKING62109.2024.10619856. 
[15] 	N. Baldo, M. Requena-Esteso, J. Nunez-Martinez, M. Portoles-Comeras, J. Nin-Guerrero, P. Dini, and J. Mangues-Bafalluy, “Validation of the IEEE 802.11 MAC Model in the ns3 Simulator Using the EXTREME Testbed,” in Proc. 3rd International ICST Conference on Simulation Tools and Techniques (SIMUTools), 2010, doi: 10.4108/ICST.SIMUTOOLS2010.8705. 
[16] 	R. Jain, D.-M. Chiu, and W. R. Hawe, “A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems,” Digital Equipment Corporation, DEC Research Report TR-301, Sep. 1984. [Online]. Available: https://www.cse.wustl.edu/~jain/papers/ftp/fairness. 
[17] 	IEEE, “IEEE Standard for Information Technology—Telecommunications and Information Exchange between Systems—Local and Metropolitan Area Networks—Specific Requirements—Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications,” IEEE Std 802.11-2020, pp. 1–4379, Feb. 2021, doi: 10.1109/IEEESTD.2021.9363693.
[18] 	A. Goldsmith, Wireless Communications. Cambridge, U.K.: Cambridge University Press, 2005, ISBN: 978-0-521-83716-3. 
[19] 	G. Bianchi, “Performance Analysis of the IEEE 802.11 Distributed Coordination Function,” IEEE Journal on Selected Areas in Communications, vol. 18, no. 3, pp. 535–547, Mar. 2000, doi: 10.1109/49.840210. 
[20] 	F. Cali, M. Conti, and E. Gregori, “Dynamic Tuning of the IEEE 802.11 Protocol to Achieve a Theoretical Throughput Limit,” IEEE/ACM Transactions on Networking, vol. 8, no. 6, pp. 785–799, Dec. 2000, doi: 10.1109/90.893874. 
[21] 	B. Bellalta, “IEEE 802.11ax: High-Efficiency WLANs,” IEEE Wireless Communications, vol. 23, no. 1, pp. 38–46, Feb. 2016, doi: 10.1109/MWC.2016.7422404. 
[22] 	E. Khorov, I. Levitsky, and I. F. Akyildiz, “Current Status and Directions of IEEE 802.11be, the Future Wi-Fi 7,” IEEE Access, vol. 8, pp. 88664–88688, 2020, doi: 10.1109/ACCESS.2020.2993448. 
[23] 	C. Deng et al., “IEEE 802.11be Wi-Fi 7: New Challenges and Opportunities,” IEEE Communications Surveys & Tutorials, vol. 22, no. 4, pp. 2136–2166, Fourth Quarter 2020, doi: 10.1109/COMST.2020.3012715. 
[24] 	D. Lopez-Perez, A. Garcia-Rodriguez, L. Galati-Giordano, M. Kasslin, and K. Doppler, “IEEE 802.11be Extremely High Throughput: The Next Generation of Wi-Fi Technology Beyond 802.11ax,” IEEE Communications Magazine, vol. 57, no. 9, pp. 113–119, Sep. 2019, doi: 10.1109/MCOM.001.1900338.
[25] 	IEEE, “IEEE Standard for Information Technology—Telecommunications and Information Exchange between Systems—Local and Metropolitan Area Networks—Specific Requirements—Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications Amendment 2: Enhancements for Extremely High Throughput (EHT),” IEEE Std 802.11be-2024, pp. 1–1020, Jul. 2025, doi: 10.1109/IEEESTD.2024.11090080.
[26] 	C. Chen, X. Chen, D. Das, D. Akhmetov, and C. Cordeiro, “Overview and Performance Evaluation of Wi-Fi 7,” IEEE Communications Standards Magazine, vol. 6, no. 2, pp. 12–18, Jun. 2022, doi: 10.1109/MCOMSTD.0001.2100082. 
[27] 	A. A. Abdalhafid, S. K. Subramaniam, Z. A. Zukarnain, and F. H. Ayob, “Multi-Link Operation in IEEE802.11be Extremely High Throughput: A Survey,” IEEE Access, vol. 12, pp. 46891–46906, 2024, doi: 10.1109/ACCESS.2024.3378997. 
[28] 	N. Korolev, I. Levitsky, I. Startsev, B. Bellalta, and E. Khorov, “Study of Multi-Link Channel Access Without Simultaneous Transmit and Receive in IEEE 802.11be Networks,” IEEE Access, vol. 10, pp. 126339–126351, 2022, doi: 10.1109/ACCESS.2022.3225978. 
[29] 	C.-L. Tai, M. Eisen, D. Akhmetov, D. Das, D. Cavalcanti, and R. Sivakumar, “Model-Free Dynamic Traffic Steering for Multi-Link Operation in IEEE 802.11be,” in Proc. IEEE International Conference on Machine Learning for Communication and Networking (ICMLCN), 2024, pp. 44–49, doi: 10.1109/ICMLCN59089.2024.10624802. 
[30] 	R. Stacey, “Multi-Band, Multi-Radio Wireless LANs and PANs,” in Proc. 43rd Asilomar Conference on Signals, Systems and Computers, 2009, pp. 317–320, doi: 10.1109/ACSSC.2009.5470088. 
[31] 	Federal Communications Commission, “Unlicensed Use of the 6 GHz Band; Expanding Flexible Use in Mid-Band Spectrum Between 3.7 and 24 GHz,” Report and Order and Further Notice of Proposed Rulemaking, FCC 20-51, ET Docket No. 18-295 and GN Docket No. 17-183, Apr. 2020. [Online]. Available: https://www.fcc.gov/document/fcc-opens-6-ghz-band-wi-fi-and-other-unlicensed-uses.
[32] 	T. Song and T. Kim, “Performance Analysis of Synchronous Multi-Radio Multi-Link MAC Protocols in IEEE 802.11be Extremely High Throughput WLANs,” Applied Sciences, vol. 11, no. 1, Art. no. 317, Jan. 2021, doi: 10.3390/app11010317. 
[33] 	R. Mahindra, H. Viswanathan, K. Sundaresan, M. Y. Arslan, and S. Rangarajan, “A Practical Traffic Management System for Integrated LTE-WiFi Networks,” in Proc. 20th Annual International Conference on Mobile Computing and Networking (MobiCom), 2014, pp. 189–200, doi: 10.1145/2639108.2639120. 
[34] 	H. Gong and J. Kim, “Dynamic Load Balancing Through Association Control of Mobile Users in WiFi Networks,” IEEE Transactions on Consumer Electronics, vol. 54, no. 2, pp. 342–348, May 2008, doi: 10.1109/TCE.2008.4560097. 
[35] 	T. S. Rappaport, Wireless Communications: Principles and Practice, 2nd ed. Upper Saddle River, NJ, USA: Prentice Hall, 2002, ISBN: 978-0-13-042232-3. 
[36] 	Y. Bejerano, S.-J. Han, and L. E. Li, “Fairness and Load Balancing in Wireless LANs Using Association Control,” in Proc. 10th Annual International Conference on Mobile Computing and Networking (MobiCom), 2004, pp. 315–329, doi: 10.1145/1023720.1023751. 
[37] 	A. Lopez-Raventos and B. Bellalta, “Concurrent Decentralized Channel Allocation and Access Point Selection Using Multi-Armed Bandits in Multi BSS WLANs,” Computer Networks, vol. 180, Art. no. 107381, Oct. 2020, doi: 10.1016/j.comnet.2020.107381. 
[38] 	A. Ali and F. A. Khan, “Condition and Location-Aware Channel Switching Scheme for Multi-Hop Multi-Band WLANs,” Computer Networks, vol. 168, Art. no. 107048, Feb. 2020, doi: 10.1016/j.comnet.2019.107048. 
[39] 	S. Barrachina-Munoz, A. Chiumento, and B. Bellalta, “Multi-Armed Bandits for Spectrum Allocation in Multi-Agent Channel Bonding WLANs,” IEEE Access, vol. 9, pp. 133472–133490, 2021, doi: 10.1109/ACCESS.2021.3114430. 
[40] 	T. Adame, M. Carrascosa, B. Bellalta, I. Pretel, and I. Etxebarria, “Channel Load Aware AP/Extender Selection in Home WiFi Networks Using IEEE 802.11k/v,” IEEE Access, vol. 9, pp. 30095–30112, 2021, doi: 10.1109/ACCESS.2021.3059473. 
[41] 	D. B. Johnson and D. A. Maltz, “Dynamic Source Routing in Ad Hoc Wireless Networks,” in Mobile Computing, T. Imielinski and H. F. Korth, Eds. Boston, MA, USA: Kluwer Academic Publishers, 1996, pp. 153–181, doi: 10.1007/978-0-585-29603-6_5. 
[42] 	K. Wehrle, M. Gunes, and J. Gross, Eds., Modeling and Tools for Network Simulation. Berlin, Germany: Springer, 2010, doi: 10.1007/978-3-642-12331-3. 
