# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PhanHoi(models.Model):
    _name = 'phan_hoi'
    _description = 'Phản hồi khách hàng'
    _rec_name = 'tieu_de'
    _order = 'ngay_phan_hoi desc'

    ma_phan_hoi = fields.Char("Mã phản hồi", readonly=True, copy=False)
    tieu_de = fields.Char("Tiêu đề", required=True)
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)

    # Thông tin phản hồi
    ngay_phan_hoi = fields.Datetime("Ngày phản hồi", default=fields.Datetime.now, required=True)
    nhan_vien_danh_gia_id = fields.Many2one('nhan_vien', string="Nhân viên được đánh giá")

    # Đánh giá theo số sao
    muc_do_hai_long = fields.Selection([
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')
    ], string="Số sao đánh giá")
    
    # Nội dung
    noi_dung_phan_hoi = fields.Text("Nội dung phản hồi", required=True)
    
    @api.model
    def create(self, vals):
        # Tạo mã phản hồi tự động
        counter = 1
        ma_phan_hoi = f"PH{counter:04d}"
        while self.search([('ma_phan_hoi', '=', ma_phan_hoi)], limit=1):
            counter += 1
            ma_phan_hoi = f"PH{counter:04d}"
        
        vals['ma_phan_hoi'] = ma_phan_hoi
        record = super(PhanHoi, self).create(vals)
        
        # Nếu đánh giá từ 1-2 sao, tự động tạo khiếu nại
        if record.muc_do_hai_long in ['1', '2']:
            self._create_complaint_from_feedback(record)
        
        return record
    
    def _create_complaint_from_feedback(self, record):
        """Tự động tạo khiếu nại từ phản hồi 1-2 sao"""
        XuLyKhieuNai = self.env['xu_ly_khieu_nai']
        
        # Xác định mức độ ưu tiên dựa trên số sao
        if record.muc_do_hai_long == '1':
            muc_do_uu_tien = 'rat_cao'
        else:  # 2 sao
            muc_do_uu_tien = 'cao'
        
        # Tạo khiếu nại mới
        complaint_vals = {
            'tieu_de_khieu_nai': f"Khiếu nại từ đánh giá {record.muc_do_hai_long} sao: {record.tieu_de}",
            'khach_hang_id': record.khach_hang_id.id,
            'ngay_khieu_nai': record.ngay_phan_hoi,
            'noi_dung_khieu_nai': record.noi_dung_phan_hoi,
            'loai_khieu_nai': 'dich_vu_khach_hang',
            'muc_do_uu_tien': muc_do_uu_tien,
            'trang_thai': 'moi',
            'nguoi_xu_ly_id': record.nhan_vien_danh_gia_id.id if record.nhan_vien_danh_gia_id else None,
        }
        
        XuLyKhieuNai.create(complaint_vals)
