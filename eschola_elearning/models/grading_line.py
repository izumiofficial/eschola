from odoo import api, fields, models

class GradingLine(models.Model):
    _name = 'grading.line'

    name = fields.Char(string='Assignment Code')
    assignments_id = fields.Many2one('assignments', string='Assignment Type')
    weightage = fields.Integer(string='Weightage')

    grading_structure_id = fields.Many2one('grading.structure', string='Grading Structure')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'grading_structure_id' in vals:
                grading = self.env['ir.sequence'].next_by_code('grading.line')
                grading_structure = self.env['grading.structure'].browse(vals['grading_structure_id'])
                register = grading_structure.course_id.id
                if register:
                    vals['name'] = str(register) + grading
                elif 'assignment_type_id' in vals:  # Check for assignment_type_id
                    vals['name'] = str(vals['assignment_id']) + grading  # Use assignment_id
                else:
                    vals['name'] = 'Default Code'  # Or handle as needed
        return super(GradingLine, self).create(vals_list)
