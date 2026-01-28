# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Quản lý hợp đồng khách hàng'
    _rec_name = 'so_hop_dong'
    _order = 'ngay_ky desc'

    so_hop_dong = fields.Char("Số hợp đồng", required=True, copy=False)
    ten_hop_dong = fields.Char("Tên hợp đồng", required=True)
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    
    # Thông tin hợp đồng
    loai_hop_dong = fields.Selection([
        ('ban_hang', 'Bán hàng'),
        ('dich_vu', 'Dịch vụ'),
        ('thue', 'Thuê'),
        ('hop_tac', 'Hợp tác'),
        ('khac', 'Khác')
    ], string="Loại hợp đồng", required=True, default='ban_hang')
    
    ngay_ky = fields.Date("Ngày ký", default=fields.Date.today, required=True)
    ngay_hieu_luc = fields.Date("Ngày hiệu lực", required=True)
    ngay_het_han = fields.Date("Ngày hết hạn")
    
    # Giá trị hợp đồng
    gia_tri_hop_dong = fields.Float("Giá trị hợp đồng", required=True)
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', 'USD'),
        ('eur', 'EUR')
    ], string="Đơn vị tiền tệ", default='vnd')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_ky', 'Đã ký'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='nhap', required=True)
    
    # Người ký
    nguoi_dai_dien = fields.Char("Người đại diện công ty")
    nguoi_ky_kh = fields.Char("Người ký (Khách hàng)")
    
    # Nội dung
    noi_dung = fields.Text("Nội dung hợp đồng")
    dieu_khoan = fields.Text("Điều khoản")
    ghi_chu = fields.Text("Ghi chú")
    
    # File đính kèm
    file_hop_dong = fields.Binary("File hợp đồng")
    file_name = fields.Char("Tên file")
    
    def action_cho_duyet(self):
        self.write({'trang_thai': 'cho_duyet'})
    
    def action_duyet(self):
        self.write({'trang_thai': 'da_ky'})
    
    def action_thuc_hien(self):
        self.write({'trang_thai': 'dang_thuc_hien'})
    
    def action_hoan_thanh(self):
        self.write({'trang_thai': 'hoan_thanh'})
    
    def action_huy(self):
        self.write({'trang_thai': 'huy'})
