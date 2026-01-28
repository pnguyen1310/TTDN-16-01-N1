# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Dự án'
    _rec_name = 'ten_du_an'
    _order = 'ngay_bat_dau desc'

    ma_du_an = fields.Char("Mã dự án", readonly=True, copy=False)
    ten_du_an = fields.Char("Tên dự án", required=True)
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    
    # Thời gian
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    # Mô tả
    mo_ta = fields.Text("Mô tả")
    
    # Ngân sách
    ngan_sach = fields.Float("Ngân sách")
    chi_phi_thuc_te = fields.Float("Chi phí thực tế")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('ke_hoach', 'Kế hoạch'),
        ('dang_tien_hanh', 'Đang tiến hành'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='ke_hoach', required=True)
    
    # Phòng ban phụ trách & nhân viên được gán tự động
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban phụ trách", required=True)
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string="Nhân viên được gán", readonly=True)
    
    # Công việc liên quan
    cong_viec_ids = fields.One2many('cong_viec', 'du_an_id', string="Công việc")
    
    # Tài nguyên dự án
    tai_nguyen_ids = fields.One2many('tai_nguyen_du_an', 'du_an_id', string="Tài nguyên")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")

    @api.onchange('phong_ban_id')
    def _onchange_phong_ban(self):
        """Auto-assign free employee when department is selected."""
        if self.phong_ban_id:
            employee = self._find_free_employee(self.phong_ban_id)
            if employee:
                self.nguoi_phu_trach_id = employee

    @api.model
    def create(self, vals):
        # Tạo mã dự án tự động
        counter = 1
        ma_du_an = f"DA{counter:04d}"
        while self.search([('ma_du_an', '=', ma_du_an)], limit=1):
            counter += 1
            ma_du_an = f"DA{counter:04d}"
        
        vals['ma_du_an'] = ma_du_an

        # Gán nhân viên rảnh trong phòng ban được chọn
        dept_id = vals.get('phong_ban_id')
        if dept_id and not vals.get('nguoi_phu_trach_id'):
            employee = self._find_free_employee(self.env['phong_ban'].browse(dept_id))
            if employee:
                vals['nguoi_phu_trach_id'] = employee.id
        return super(DuAn, self).create(vals)
    
    def action_bat_dau(self):
        self.write({'trang_thai': 'dang_tien_hanh'})
    
    def action_hoan_thanh(self):
        self.write({'trang_thai': 'hoan_thanh'})
    
    def action_huy(self):
        self.write({'trang_thai': 'huy'})

    def write(self, vals):
        # Nếu đổi phòng ban và chưa có người, tự gán lại
        if 'phong_ban_id' in vals and not vals.get('nguoi_phu_trach_id'):
            dept_id = vals.get('phong_ban_id') or self.phong_ban_id.id
            if dept_id:
                employee = self._find_free_employee(self.env['phong_ban'].browse(dept_id))
                if employee:
                    vals['nguoi_phu_trach_id'] = employee.id
        return super().write(vals)

    def _find_free_employee(self, department):
        """Tìm nhân viên trong phòng ban chưa phụ trách công việc/dự án đang mở."""
        if not department:
            return False
        employees = self.env['nhan_vien'].search([('phong_ban_id', '=', department.id)])
        for emp in employees:
            active_tasks = self.env['cong_viec'].search_count([
                ('nguoi_thuc_hien_id', '=', emp.id),
                ('trang_thai', 'in', ['moi', 'dang_thuc_hien'])
            ])
            active_projects = self.env['du_an'].search_count([
                ('nguoi_phu_trach_id', '=', emp.id),
                ('trang_thai', 'in', ['ke_hoach', 'dang_tien_hanh', 'tam_dung'])
            ])
            if active_tasks == 0 and active_projects == 0:
                return emp
        return employees[:1] if employees else False
