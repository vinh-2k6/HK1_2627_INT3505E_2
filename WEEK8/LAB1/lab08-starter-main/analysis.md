# Phân tích kết quả Load Test (Lab 4)

## Bảng tổng hợp kết quả
| Kịch bản | Users | p95 | RPS | Tỷ lệ lỗi |
|---|---:|---:|---:|---:|
| A (Baseline) | 10 | ~10 ms | ~5.8 | ~1.7% |
| B (Normal Load) | 50 | ~9 ms | ~27.4 | ~0.3% |
| C (Spike Test) | 200 | ~28 ms | ~113.8 | ~0.4% |

## Trả lời các câu hỏi phân tích

1. **Trong 3 kịch bản, kịch bản nào có p95 cao nhất? Vì sao?**
   - Kịch bản C có p95 cao nhất (lên tới ~28ms) do số lượng người dùng đồng thời tăng vọt đột ngột lên 200 user (spike test), khiến hệ thống Flask chạy cục bộ bị dồn ứ request, làm tăng độ trễ phản hồi.

2. **Có endpoint nào fail rate tăng theo số user? Đoán nguyên nhân dựa trên code.**
   - Endpoint `/books/search?year={year}` có tỷ lệ lỗi tăng theo số lượng request. Nguyên nhân là do trong `locustfile.py`, task `search_by_year` được chủ động cấu hình trả về lỗi `500` với xác suất 1% (`random.random() < 0.01`). Khi số lượng user tăng, tổng số request gọi vào endpoint này lớn hơn, kéo theo số lượng request lỗi 500 tăng theo.

3. **Nếu prod cần SLO p95 < 300ms, kịch bản nào đạt? Đề xuất baseline cho CI gate.**
   - Cả 3 kịch bản A, B, C đều có p95 rất thấp (dưới 30ms), hoàn toàn đáp ứng tốt SLO `p95 < 300ms`. 
   - Đề xuất lấy **Kịch bản A** (10 users) làm ngưỡng baseline chuẩn cho CI gate vì nó phản ánh chính xác tải nhẹ khi kiểm thử tự động.

4. **Câu hỏi bonus (Connection pool giới hạn 5):**
   - Khi connection pool giới hạn 5 mà có 200 user truy cập đồng thời, 195 user sẽ phải xếp hàng chờ kết nối cơ sở dữ liệu. Điều này làm thời gian chờ (latency, p95/p99) tăng vọt đột biến và có thể xuất hiện lỗi timeout. Có thể xác nhận điều này qua biểu đồ Response Time và số lượng Failure tăng cao trong báo cáo HTML của Locust.