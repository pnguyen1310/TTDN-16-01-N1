# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TaiNguyenDuAn(models.Model):
    _name = 'tai_nguyen_du_an'
    _description = 'Tài nguyên dự án'
    _rec_name = 'ten_tai_nguyen'

    du_an_id = fields.Many2one('du_an', string="Dự án", required=True, ondelete='cascade')
    ten_tai_nguyen = fields.Char("Tên tài nguyên", required=True)
    loai_tai_nguyen = fields.Selection([
        ('nhan_luc', 'Nhân lực'),
        ('thiet_bi', 'Thiết bị'),
        ('chi_phi', 'Chi phí'),
        ('van_de', 'Vật liệu'),
        ('khac', 'Khác')
    ], string="Loại tài nguyên", required=True, default='nhan_luc')
    
    # Nhân viên phụ trách (nếu là nhân lực)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên")
    
    # Số lượng/Giá trị
    so_luong = fields.Float("Số lượng")
    gia_tri = fields.Float("Giá trị")
    
    # Thời gian sử dụng
    ngay_bat_dau = fields.Date("Ngày bắt đầu")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('co_san', 'Còn sẵn'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('khong_co_san', 'Không còn sẵn')
    ], string="Trạng thái", default='co_san')
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
