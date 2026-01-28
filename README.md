 <h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   Hệ thống quản lý nhân sự, khách hàng và công việc trên nền tảng Odoo 15
</h2>
<div align="center">
    <p align="center">
        <img src="images/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="images/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="images/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
</div>

## 1. Tổng quan về hệ thống

Hệ thống được xây dựng trên nền tảng Odoo 15 nhằm hỗ trợ doanh nghiệp quản lý tập trung các nghiệp vụ cốt lõi, bao gồm quản lý nhân sự, quản lý khách hàng và quản lý công việc. Hệ thống được thiết kế theo mô hình ERP module hóa, cho phép các chức năng liên kết chặt chẽ với nhau, đồng thời đảm bảo tính linh hoạt, dễ mở rộng và phù hợp với nhu cầu quản lý thực tế của doanh nghiệp.

Trong hệ thống, mỗi nghiệp vụ được triển khai dưới dạng một module độc lập nhưng có khả năng tích hợp và chia sẻ dữ liệu. Nhờ đó, thông tin về nhân sự, khách hàng, công việc và phản hồi được quản lý đồng bộ, giúp nâng cao hiệu quả vận hành, giảm thao tác thủ công và hỗ trợ nhà quản lý trong quá trình theo dõi, đánh giá và ra quyết định.

Bên cạnh các chức năng quản lý cơ bản, hệ thống còn tích hợp một số tính năng mở rộng như tự động hóa quy trình chăm sóc khách hàng, xử lý khiếu nại, đồng bộ lịch công việc với Google Calendar và chatbot nội quy hỗ trợ tra cứu quy định công ty. Các tính năng này góp phần nâng cao trải nghiệm người dùng và tiệm cận hơn với nhu cầu thực tế của doanh nghiệp hiện nay.

## 2. Các chức năng chính

Hệ thống cung cấp các chức năng quản lý nghiệp vụ cốt lõi của doanh nghiệp, được triển khai dưới dạng các module độc lập nhưng có khả năng liên kết và chia sẻ dữ liệu với nhau.

### 2.1. Quản lý nhân sự
- Quản lý thông tin nhân viên, phòng ban và chức vụ.
- Phân quyền người dùng theo vai trò.
- Liên kết nhân viên với công việc và khách hàng phụ trách.

### 2.2. Quản lý khách hàng
- Quản lý thông tin khách hàng và hợp đồng.
- Theo dõi phản hồi và đánh giá của khách hàng.
- Quản lý và triển khai các chiến dịch marketing.
- Tự động tạo chiến dịch sinh nhật khách hàng.

### 2.3. Quản lý công việc
- Tạo và theo dõi công việc theo trạng thái.
- Quản lý dự án và tài nguyên dự án.
- Phân công công việc cho nhân viên.
- Tự động tạo công việc xử lý khiếu nại khi phản hồi khách hàng có đánh giá thấp.

### 2.4. Tích hợp lịch làm việc
- Đồng bộ thời gian công việc với Google Calendar.
- Hỗ trợ theo dõi lịch làm việc theo ngày, tuần, tháng.
- Giảm trùng lịch và bỏ sót công việc.

### 2.5. Chatbot nội quy
- Hỗ trợ tra cứu nội quy và quy định công ty.
- Chatbot sử dụng Groq API để xử lý câu hỏi.
- Trả lời dựa trên dữ liệu nội quy được cấu hình sẵn trong hệ thống.

## 3. Công nghệ sử dụng

![OS](https://img.shields.io/badge/OS-Ubuntu-orange?logo=ubuntu&logoColor=white)
![ERP](https://img.shields.io/badge/ERP-Odoo%2015-purple)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue?logo=postgresql&logoColor=white)
![Container](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=white)
![Repository](https://img.shields.io/badge/Repository-GitHub-black?logo=github&logoColor=white)

Hệ thống được triển khai trên hệ điều hành Ubuntu, sử dụng nền tảng Odoo 15 làm lõi ERP.  
Python 3.10 được sử dụng để phát triển các module nghiệp vụ, kết hợp với PostgreSQL để lưu trữ dữ liệu.  
Docker hỗ trợ triển khai cơ sở dữ liệu, trong khi GitHub được dùng để quản lý mã nguồn.  
Ngoài ra, hệ thống tích hợp Google Calendar API và Groq API để mở rộng chức năng.


## 4. Cài đặt công cụ, môi trường và các thư viện cần thiết

### 4.1. Clone project.
```
git clone https://github.com/pnguyen1310/TTDN-16-01-N1.git
git checkout 
```
### 4.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
### 4.3. khởi tạo môi trường ảo.

`python3.10 -m venv ./venv`
Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
pip3 install -r requirements.txt
```

### 4.4. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.

`docker-compose up -d`

### 4.5. Setup tham số chạy cho hệ thống
#### Khởi tạo odoo.conf
Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5432
xmlrpc_port = 8069
```
Có thể kế thừa từ **odoo.conf.template**

Ngoài ra có thể thêm mổ số parameters như:

```
-c _<đường dẫn đến tệp odoo.conf>_
-u _<tên addons>_ giúp cập nhật addons đó trước khi khởi chạy
-d _<tên database>_ giúp chỉ rõ tên database được sử dụng
--dev=all giúp bật chế độ nhà phát triển 
```

### 4.7. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

##  5. Hình ảnh các giao diện
###  Giao diện Dashboard
<p align="center">
  <img src="images/Capture1.PNG" alt="Giao diện Dashboard" width="450" />
  <br>
 <em> Hình 1: Giao diện Dashboard </em>
</p>

###  Giao diện quản lý nhân sự
<p align="center">
  <img src="images/Capture2.PNG" alt="Giao diện quản lý nhân sự" width="450" />
  <br>
 <em> Hình 2: Giao diện quản lý nhân sự </em>
</p>

###  Giao diện phản Chatbot hỗ trợ giải đáp nội quy
<p align="center">
  <img src="images/Capture3.PNG" alt="Giao diện phản Chatbot hỗ trợ giải đáp nội quy" width="450" />
  <br>
<em> Hình 3: Giao diện phản Chatbot hỗ trợ giải đáp nội quy </em>
</p>

###  Giao diện quản lý khách hàng
<p align="center">
  <img src="images/Capture4.PNG" alt="Giao diện quản lý khách hàng" width="450" />
  <br>
<em> Hình 4: Giao diện quản lý khách hàng </em>
</p>

###  Giao diện chiến dịch marketing
<p align="center">
  <img src="images/Capture5.PNG" alt="Giao diện chiến dịch marketing" width="450" />
  <br>
<em> Hình 5: Giao diện chiến dịch marketing </em>
</p>

###  Giao diện quản lý công việc
<p align="center">
  <img src="images/Capture6.PNG" alt="Giao diện quản lý công việc" width="450" />
  <br>
<em> Hình 6: Giao diện quản lý công việc </em>
</p>

###  Giao diện lịch đồng bộ với quản lý công việc
<p align="center">
  <img src="images/Capture7.PNG" alt="Giao diện lịch đồng bộ với quản lý công việc" width="450" />
  <br>
<em> Hình 7: Giao diện lịch đồng bộ với quản lý công việc </em>
</p>

## 📞 6. Liên hệ
- 👨‍🎓 **Sinh viên thực hiện**: Nguyễn Đào Phúc Nguyên
- 🎓 **Khoa**: Công nghệ thông tin – Đại học Đại Nam
- 📧 **Email**: nguyendaophucnguyen13@gmail.com
