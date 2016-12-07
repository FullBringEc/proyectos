#-*- coding: utf-8 -*-
from openerp import models, fields, api

class Tag(models.Model):
    _name = 'todo.task.tag'
    name = fields.Char('Name', size = 40, translate=True)

class Stage(models.Model):
    _name  = 'todo.task.stage'
    _order = 'sequence,name'

    # Campos de cadena de caracteres:
    name  = fields.Char('Name',size = 40)
    desc  = fields.Text('Description')
    state = fields.Selection([('draft','New'),('open','Started'), ('done','Closed')],'State')
    docs  = fields.Html('Documentation')

    # Campos numéricos:
    sequence      = fields.Integer('Sequence')
    perc_complete = fields.Float('Complete',(3,2))

    # Campos de fecha:
    date_effective = fields.Date('Effective Date')
    date_changed   = fields.Datetime('Last Changed')

    # Otros campos:
    fold  = fields.Boolean('Folded?')
    image = fields.Binary('Image')

class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
    stage_fold = fields.Boolean('Stage Folded?', compute='_compute_stage_fold')
    
    stage_state = fields.Selection(related='stage_id.state', string='Stage State')

    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
    	self.stage_fold = self.stage_id.fold


    @api.one 
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)])

    user_todo_count = fields.Integer('User To-Do   Count', compute='compute_user_todo_count')