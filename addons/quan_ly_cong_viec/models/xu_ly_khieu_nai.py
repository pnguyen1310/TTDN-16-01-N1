# -*- coding: utf-8 -*-
from odoo import models, fields, api


class XuLyKhieuNai(models.Model):
    _name = 'xu_ly_khieu_nai'
    _description = 'Xử lý khiếu nại khách hàng'
    _rec_name = 'tieu_de_khieu_nai'
    _order = 'ngay_khieu_nai desc'

    ma_khieu_nai = fields.Char("Mã khiếu nại", readonly=True, copy=False)
    tieu_de_khieu_nai = fields.Char("Tiêu đề khiếu nại", required=True)
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    
    # Thời gian
    ngay_khieu_nai = fields.Datetime("Ngày khiếu nại", default=fields.Datetime.now, required=True)
    ngay_xu_ly = fields.Date("Ngày xử lý")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    # Nội dung
    noi_dung_khieu_nai = fields.Text("Nội dung khiếu nại", required=True)
    
    # Loại khiếu nại
    loai_khieu_nai = fields.Selection([
        ('chat_luong', 'Chất lượng sản phẩm/dịch vụ'),
        ('giao_hang', 'Giao hàng/Vận chuyển'),
        ('gia_ca', 'Giá cả'),
        ('dich_vu_khach_hang', 'Dịch vụ khách hàng'),
        ('khac', 'Khác')
    ], string="Loại khiếu nại", required=True, default='khac')
    
    # Mức độ ưu tiên
    muc_do_uu_tien = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('rat_cao', 'Rất cao')
    ], string="Mức độ ưu tiên", default='trung_binh')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_xu_ly', 'Đang xử lý'),
        ('da_phan_hoi', 'Đã phản hồi'),
        ('hoan_thanh', 'Hoàn thành'),
        ('tu_choi', 'Từ chối')
    ], string="Trạng thái", default='moi', required=True)
    
    # Người xử lý
    nguoi_xu_ly_id = fields.Many2one('nhan_vien', string="Người xử lý")
    
    # Xử lý
    phan_hoi_xu_ly = fields.Text("Phản hồi xử lý")
    giai_phap = fields.Text("Giải pháp đề xuất")
    
    # Kết quả
    ket_qua = fields.Selection([
        ('chap_nhan', 'Chấp nhận'),
        ('tu_choi', 'Từ chối'),
        ('phan_nua', 'Phân nửa'),
        ('cho_xac_nhan', 'Chờ xác nhận')
    ], string="Kết quả xử lý")
    
    # Bồi thường
    so_tien_boi_thuong = fields.Float("Số tiền bồi thường")
    ghi_chu = fields.Text("Ghi chú")

    @api.model
    def create(self, vals):
        # Tạo mã khiếu nại tự động
        counter = 1
        ma_khieu_nai = f"KN{counter:04d}"
        while self.search([('ma_khieu_nai', '=', ma_khieu_nai)], limit=1):
            counter += 1
            ma_khieu_nai = f"KN{counter:04d}"
        
        vals['ma_khieu_nai'] = ma_khieu_nai
        return super(XuLyKhieuNai, self).create(vals)
    
    def action_bat_dau_xu_ly(self):
        self.write({'trang_thai': 'dang_xu_ly', 'ngay_xu_ly': fields.Date.today()})
    
    def action_phan_hoi(self):
        self.write({'trang_thai': 'da_phan_hoi'})
    
    def action_hoan_thanh(self):
        self.write({'trang_thai': 'hoan_thanh', 'ngay_ket_thuc': fields.Date.today()})
    
    def action_tu_choi(self):
        self.write({'trang_thai': 'tu_choi'})
