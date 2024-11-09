# Xây dựng hệ thống tìm kiếm ảnh dựa trên mô tả

## Mục tiêu
Hệ thống này cho phép tìm kiếm hình ảnh dựa trên đoạn mô tả văn bản, giúp người dùng nhanh chóng tìm thấy ảnh mong muốn thông qua một đoạn văn mô tả. 

## Kiến thức cần nghiên cứu
Để xây dựng hệ thống, cần nghiên cứu và áp dụng các kiến thức sau:

- **Text Embedding Models**: Sử dụng các mô hình ngôn ngữ như:
  - BERT (Bidirectional Encoder Representations from Transformers)
  - Sentence Transformers
  - CLIP (Contrastive Language-Image Pretraining)

  Các mô hình này sẽ được dùng để nhúng văn bản và hình ảnh vào cùng một không gian vector, giúp so khớp giữa đoạn mô tả và ảnh.

- **Vector Search**: Tìm hiểu các phương pháp tìm kiếm dựa trên vector để xử lý và tìm kiếm dữ liệu nhúng, bao gồm:
  - FAISS (Facebook AI Similarity Search): Công cụ mạnh mẽ cho phép tìm kiếm và so khớp nhanh chóng trong không gian vector.

- **Kỹ thuật Embedding**: Đảm bảo rằng văn bản mô tả và đặc trưng của ảnh có thể được biểu diễn và so sánh trong cùng không gian nhúng, giúp đạt hiệu quả cao khi tìm kiếm.

## Ứng dụng
Hệ thống tìm kiếm ảnh theo mô tả này có thể được áp dụng vào nhiều trường hợp thực tiễn, ví dụ như Hỗ trợ người dùng tìm kiếm các hình ảnh trong thư viện cá nhân **Google Photos**.
