# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ChienDich(models.Model):
    _name = 'chien_dich'
    _description = 'Chiến dịch Marketing'
    _rec_name = 'ten_chien_dich'
    _order = 'ngay_bat_dau desc'

    ma_chien_dich = fields.Char("Mã chiến dịch", readonly=True, copy=False)
    ten_chien_dich = fields.Char("Tên chiến dịch", required=True)
    
    # Loại chiến dịch
    loai_chien_dich = fields.Selection([
        ('email', 'Email Marketing'),
        ('sms', 'SMS Marketing'),
        ('social', 'Social Media'),
        ('quang_cao', 'Quảng cáo'),
        ('su_kien', 'Sự kiện'),
        ('khuyen_mai', 'Khuyến mãi'),
        ('khac', 'Khác')
    ], string="Loại chiến dịch", required=True, default='email')
    
    # Thời gian
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    # Ngân sách
    ngan_sach = fields.Float("Ngân sách")
    chi_phi_thuc_te = fields.Float("Chi phí thực tế")
    
    # Mục tiêu
    muc_tieu = fields.Text("Mục tiêu chiến dịch")
    doi_tuong_muc_tieu = fields.Text("Đối tượng mục tiêu")
    
    # KPI
    so_khach_hang_muc_tieu = fields.Integer("Số khách hàng mục tiêu")
    so_khach_hang_tiep_can = fields.Integer("Số khách hàng tiếp cận")
    ty_le_chuyen_doi = fields.Float("Tỷ lệ chuyển đổi (%)", compute="_compute_ty_le_chuyen_doi")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('ke_hoach', 'Kế hoạch'),
        ('dang_chay', 'Đang chạy'),
        ('tam_dung', 'Tạm dừng'),
        ('ket_thuc', 'Kết thúc'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='ke_hoach', required=True)
    
    # Người phụ trách
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string="Người phụ trách")
    
    # Nội dung
    noi_dung = fields.Html("Nội dung chiến dịch")
    ket_qua = fields.Text("Kết quả đạt được")
    ghi_chu = fields.Text("Ghi chú")
    
    # Danh sách khách hàng tham gia
    khach_hang_ids = fields.Many2many('khach_hang', string="Khách hàng tham gia")
    so_luong_khach_hang = fields.Integer("Số lượng khách hàng", compute="_compute_so_luong_khach_hang")
    
    @api.depends('khach_hang_ids')
    def _compute_so_luong_khach_hang(self):
        for record in self:
            record.so_luong_khach_hang = len(record.khach_hang_ids)
    
    @api.depends('so_khach_hang_muc_tieu', 'so_khach_hang_tiep_can')
    def _compute_ty_le_chuyen_doi(self):
        for record in self:
            if record.so_khach_hang_muc_tieu > 0:
                record.ty_le_chuyen_doi = (record.so_khach_hang_tiep_can / record.so_khach_hang_muc_tieu) * 100
            else:
                record.ty_le_chuyen_doi = 0
    
    @api.model
    def create(self, vals):
        # Tạo mã chiến dịch tự động
        counter = 1
        ma_chien_dich = f"CD{counter:04d}"
        while self.search([('ma_chien_dich', '=', ma_chien_dich)], limit=1):
            counter += 1
            ma_chien_dich = f"CD{counter:04d}"
        
        vals['ma_chien_dich'] = ma_chien_dich
        return super(ChienDich, self).create(vals)
    
    def action_bat_dau(self):
        self.write({'trang_thai': 'dang_chay'})
    
    def action_tam_dung(self):
        self.write({'trang_thai': 'tam_dung'})
    
    def action_ket_thuc(self):
        self.write({'trang_thai': 'ket_thuc'})
    
    def action_huy(self):
        self.write({'trang_thai': 'huy'})
    
    @api.model
    def _cron_update_expired_campaigns(self):
        """Cron job: Tự động kết thúc chiến dịch hết hạn"""
        today = fields.Date.today()
        
        # Tìm các chiến dịch đang chạy và hết hạn
        expired_campaigns = self.search([
            ('trang_thai', '=', 'dang_chay'),
            ('ngay_ket_thuc', '<=', today),
            ('ngay_ket_thuc', '!=', False)
        ])
        
        if expired_campaigns:
            expired_campaigns.write({'trang_thai': 'ket_thuc'})
