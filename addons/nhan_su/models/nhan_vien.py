from odoo import models, fields, api
import unicodedata


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'

    ma_dinh_danh = fields.Char("Mã định danh", readonly=True, copy=False)
    ho_ten_dem = fields.Char("Họ và tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_ten_day_du = fields.Char("Họ tên đầy đủ", compute="_compute_ho_ten_day_du", store=True)
    chuc_vu = fields.Char("Chức vụ")
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác')
    ], string="Giới tính")
    so_dien_thoai = fields.Char("Số điện thoại")
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban")

    @api.depends('ho_ten_dem', 'ten')
    def _compute_ho_ten_day_du(self):
        """Tính toán họ tên đầy đủ"""
        for record in self:
            record.ho_ten_day_du = f"{record.ho_ten_dem} {record.ten}".strip()

    def name_get(self):
        """Hiển thị họ tên đầy đủ trong dropdown"""
        result = []
        for record in self:
            name = f"{record.ho_ten_dem} {record.ten}".strip()
            result.append((record.id, name))
        return result

    def _remove_accents(self, text):
        """Bỏ dấu tiếng Việt"""
        # Xử lý đặc biệt cho Đ/đ
        text = text.replace('Đ', 'D').replace('đ', 'd')
        # Bỏ dấu các ký tự khác
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        return text

    @api.onchange('ho_ten_dem', 'ten')
    def _onchange_ma_dinh_danh(self):
        """Hiển thị preview mã định danh khi nhập họ tên"""
        if self.ho_ten_dem and self.ten:
            ho_ten_dem_khong_dau = self._remove_accents(self.ho_ten_dem)
            ten_khong_dau = self._remove_accents(self.ten)
            
            ma_ho_ten_dem = ''.join([word[0].upper() for word in ho_ten_dem_khong_dau.split()])
            ma_ten = ''.join([word[0].upper() for word in ten_khong_dau.split()])
            ma_co_ban = ma_ho_ten_dem + ma_ten
            
            # Luôn bắt đầu từ 01
            counter = 1
            ma_dinh_danh = f"{ma_co_ban}{counter:02d}"
            while self.search([('ma_dinh_danh', '=', ma_dinh_danh), ('id', '!=', self.id or 0)], limit=1):
                counter += 1
                ma_dinh_danh = f"{ma_co_ban}{counter:02d}"
            
            self.ma_dinh_danh = ma_dinh_danh

    @api.model
    def create(self, vals):
        if vals.get('ho_ten_dem') and vals.get('ten'):
            # Bỏ dấu và tạo mã từ họ tên đệm + tên
            ho_ten_dem_khong_dau = self._remove_accents(vals['ho_ten_dem'])
            ten_khong_dau = self._remove_accents(vals['ten'])
            
            # Lấy chữ cái đầu của mỗi từ
            ma_ho_ten_dem = ''.join([word[0].upper() for word in ho_ten_dem_khong_dau.split()])
            ma_ten = ''.join([word[0].upper() for word in ten_khong_dau.split()])
            ma_co_ban = ma_ho_ten_dem + ma_ten
            
            # Luôn bắt đầu từ 01
            counter = 1
            ma_dinh_danh = f"{ma_co_ban}{counter:02d}"
            while self.search([('ma_dinh_danh', '=', ma_dinh_danh)], limit=1):
                counter += 1
                ma_dinh_danh = f"{ma_co_ban}{counter:02d}"
            
            vals['ma_dinh_danh'] = ma_dinh_danh
        
        return super(NhanVien, self).create(vals)

