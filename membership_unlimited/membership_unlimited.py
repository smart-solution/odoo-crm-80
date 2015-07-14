# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from datetime import datetime
from datetime import time
from datetime import date
from dateutil.relativedelta import relativedelta
from mx import DateTime
import time
import logging

logger = logging.getLogger(__name__)

STATE = [
    ('none', 'Non Member'),
    ('canceled', 'Cancelled Member'),
    ('old', 'Old Member'),
    ('waiting', 'Waiting Member'),
    ('invoiced', 'Invoiced Member'),
    ('free', 'Free Member'),
    ('paid', 'Paid Member'),
]

STATE_PRIOR = {
    'none': 0,
    'canceled': 1,
    'old': 2,
    'waiting': 3,
    'invoiced': 4,
    'free': 6,
    'paid': 7
}

INVOICE_STATE_SELECTION = [
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled')
]

class product_template(osv.osv):
    _inherit = 'product.template'
    
    _columns = {
        'membership_product': fields.boolean('Lidmaatschap'),
        'membership_combi': fields.boolean('Combi lidmaatschap'),
		'membership_combi_ids': fields.many2many('product.template', 'membership_combi_product_rel', 'parent_product_id', 'child_product_id', 'Combi-producten'),
    }
    
product_template()

class account_journal(osv.osv):
    _inherit = 'account.journal'
    
    _columns = {
        'membership_journal': fields.boolean('Dagboek Lidmaatschap'),
    }
    
account_journal()

class membership_cancel_reason(osv.osv):
    _name = 'membership.cancel.reason'

    _columns = {
        'name': fields.char('Name', len=64, select=True),
        'ref': fields.char('Code', len=32),
    }

membership_cancel_reason()

class membership_partner_account(osv.osv):
    _name = 'membership.partner.account'

    def _get_membership_lines(self, cr, uid, ids, context=None):
        list_membership_line = []
        member_line_obj = self.pool.get('membership.partner.account')
        for invoice in self.pool.get('account.invoice').browse(cr, uid, ids, context=context):
            if invoice.membership_id:
                list_membership_line.append(invoice.membership_id.id)
        return list_membership_line

    def _state(self, cr, uid, ids, name, args, context=None):
        """Compute the state lines
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Membership Line IDs
        @param name: Field Name
        @param context: A standard dictionary for contextual values
        @param return: Dictionary of state Value
        """
        res = {}
        today = time.strftime('%Y-%m-%d')
        inv_obj = self.pool.get('account.invoice')
        for line in self.browse(cr, uid, ids, context=context):
            cr.execute('''
            SELECT i.state, i.id FROM
            account_invoice i
            WHERE
            i.membership_id = %s
            ORDER BY
            i.id desc
            LIMIT 1
            ''', (line.id,))
            fetched = cr.fetchone()
            if not fetched:
                res[line.id] = 'none'
                continue
            istate = fetched[0]
            state = 'none'
            if (istate == 'draft') | (istate == 'proforma'):
                state = 'waiting'
            elif istate == 'open':
                state = 'invoiced'
            elif istate == 'paid':
                state = 'paid'
                inv = inv_obj.browse(cr, uid, fetched[1], context=context)
                for payment in inv.payment_ids:
                    if payment.invoice and payment.invoice.type == 'out_refund':
                        state = 'canceled'
            elif istate == 'cancel':
                state = 'canceled'
            if line.membership_end and today > line.membership_end:
                state = 'old'
            if line.membership_cancel and today > line.membership_cancel:
                state = 'canceled'
            res[line.id] = state
        return res

    def _get_memberships(self, cr, uid, ids, context=None):
        ids2 = ids
        return ids

    _columns = {
		'partner_id': fields.many2one('res.partner', 'Partner', select=True),
        'membership_amount': fields.float('Bedrag Lidmaatschap'),
        'membership_start': fields.date('Startdatum Lidmaatschap'),
        'membership_end': fields.date('Einddatum Lidmaatschap'),
        'membership_cancel': fields.date('Annulatie Lidmaatschap'),
        'cancel_reason_id': fields.many2one('membership.cancel.reason', 'Reden Annulatie', select=True),
        'interval_type': fields.selection((('y','Jaar'),('m','Maand'),('w','Week'),('d','Dag')), 'Interval Type'),
        'interval_number': fields.integer('Interval Aantal'),
        'last_invoice_date': fields.date('Datum Laatste Facturatie'),
        'next_invoice_date': fields.date('Datum Volgende Facturatie'),
        'product_id': fields.many2one('product.product', 'Product', select=True),
        'state': fields.function(_state,
                        string='Membership Status', type='selection',
                        selection=STATE, store = {
                        'account.invoice': (_get_membership_lines, ['state'], 10),
                        'membership.partner.account': (_get_memberships, ['membership_end', 'membership_cancel', 'membership_start'], 10)
                        }, help="""It indicates the membership status.
                        -Non Member: A member who has not applied for any membership.
                        -Cancelled Member: A member who has cancelled his membership.
                        -Old Member: A member whose membership date has expired.
                        -Waiting Member: A member who has applied for the membership and whose invoice is going to be created.
                        -Invoiced Member: A member whose invoice has been created.
                        -Paid Member: A member who has paid the membership amount."""),
        'nbr_inv_year': fields.selection((('1','1'),('2','2'),('3','3'),('4','4'),('6','6'),('12','12')),'Aantal facturen per jaar'),
    }

    def _create_membership_invoices(self, cr, uid, context=None):
        logger.info('Searching for memberships that must be invoiced')
        date_invoice = datetime.today()
#        expire_limit_date = datetime.today() + \
#            relativedelta(months=-NUMBER_OF_UNUSED_MONTHS_BEFORE_EXPIRY)
#        expire_limit_date_str = expire_limit_date.strftime('%Y-%m-%d')
        membership_ids = self.search(cr, uid, [
            '|',
            ('next_invoice_date', '=', False),
            ('next_invoice_date', '<=', date_invoice),
            ('membership_start', '<=', date_invoice),
            ('membership_cancel', '=', False),
            ], context=context)
        if membership_ids:
            self.create_membership_invoice(cr, uid, membership_ids, product_id=None, datas=None, context=context)
        else:
            logger.info('0 membership invoices created')
        return True

    def create_membership_invoice(self, cr, uid, ids, product_id=None, datas=None, context=None):
        start_time = time.time()
        id_list = []

        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        invoice_tax_obj = self.pool.get('account.invoice.tax')
        partner_obj = self.pool.get('res.partner')
        journal_obj = self.pool.get('account.journal')
        membership_line_obj = self.pool.get('membership.invoice.line')

        invoice_list = []
        for membership in self.browse(cr, uid, ids, context=context):
            if context == None:
                context = {}
                context['uid'] = 1
                context['tz'] = 'Europe/Brussels'
                context['lang'] = 'en_US'
                context['active_model'] = 'membership.partner.account'
            context['active_ids'] = [membership.id]
            context['active_id'] = membership.id
            
            product_id = membership.product_id.id
            partner_id = membership.partner_id.id
            company_id = membership.product_id.company_id.id
            journal_id = None
            journals = journal_obj.search(cr, uid, [('membership_journal','=',True)], context=context)
            if journals:
                for journal in journal_obj.browse(cr, uid, journals, context=context):
                    journal_id = journal.id

            amount_inv = membership.membership_amount

            account_id = membership.partner_id.property_account_receivable and membership.partner_id.property_account_receivable.id or False
            fpos_id = membership.partner_id.property_account_position and membership.partner_id.property_account_position.id or False
            addr = partner_obj.address_get(cr, uid, [membership.partner_id.id], ['invoice'])
            if not addr.get('invoice', False):
                raise osv.except_osv(_('Error!'),
                        _("Partner doesn't have an address to make the invoice."))

            quantity = 1

            line_value =  {
                'product_id': product_id,
            }

            payment_term_id = None
            mandate_id = None
            partner_bank_id = None
            sql_stat = '''select sdd_mandate.id as mandate_id, account_payment_term.id as payment_term_id, res_partner_bank.id as partner_bank_id from res_partner, res_partner_bank, sdd_mandate, account_payment_term
where res_partner.id = res_partner_bank.partner_id
  and partner_bank_id = res_partner_bank.id
  and sdd_mandate.state = 'valid'
  and account_payment_term.name = 'Direct debit'
  and res_partner.id = %d
order by res_partner_bank.sequence''' % (partner_id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['payment_term_id']:
                payment_term_id = sql_res['payment_term_id']
                mandate_id = sql_res['mandate_id']
                partner_bank_id = sql_res['partner_bank_id']

            line_dict = invoice_line_obj.product_id_change(cr, uid, {}, product_id, False, quantity, '', 'out_invoice', partner_id, fpos_id, price_unit=amount_inv, context=context)
            line_value.update(line_dict['value'])
            line_value['price_unit'] = amount_inv
            if line_value.get('invoice_line_tax_id', False):
                tax_tab = [(6, 0, line_value['invoice_line_tax_id'])]
                line_value['invoice_line_tax_id'] = tax_tab

            ref_type = 'none'
            reference = ''
            referenc2 = ''
#            ref_type = 'bba'
#            reference = invoice_obj.generate_bbacomm(cr, uid, ids, 'out_invoice', 'bba', partner_id, '', context={})
#            referenc2 = reference['value']['reference']

            today = datetime.today()
            datedue = datetime.today() + relativedelta(days=30)

            invoice_id = invoice_obj.create(cr, uid, {
                'partner_id': partner_id,
                'account_id': account_id,
                'membership_invoice': True,
                'fiscal_position': fpos_id or False,
                'payment_term': payment_term_id,
                'sdd_mandate_id': mandate_id,
                'partner_bank_id': partner_bank_id,
                'reference_type': ref_type,
                'type': 'out_invoice',
                'reference': referenc2,
                'date_due': datedue,
                'date_invoice': today,
                'membership_id': membership.id,
                'company_id': company_id,
                'journal_id': journal_id,
            }, context=dict(context, no_store_function=True)) # Don't store function fields inside the loop.

            invoice_list = []
            line_value['invoice_id'] = invoice_id
            if membership.product_id.product_tmpl_id.membership_combi_ids:
                invoice_line_id = []
                for combi in membership.product_id.product_tmpl_id.membership_combi_ids:
                    list_price = combi.list_price
                    if membership.interval_type == 'y' and membership.interval_number and membership.interval_number > 1:
                        list_price = list_price * membership.interval_number
                    if membership.interval_type == 'm' and membership.interval_number:
                        if membership.interval_number < 1 or membership.interval_number > 12:
                            list_price = list_price / 12
                        else:
                            list_price = list_price / 12 * membership.interval_number
                    if membership.interval_type == 'w' and membership.interval_number:
                        if membership.interval_number < 1 or membership.interval_number > 52:
                            list_price = list_price / 52
                        else:
                            list_price = list_price / 52 * membership.interval_number
                    if membership.interval_type == 'd' and membership.interval_number:
                        if membership.interval_number < 1 or membership.interval_number > 365:
                            list_price = list_price / 365
                        else:
                            list_price = list_price / 365 * membership.interval_number
                    line_value['price_unit'] = list_price
                    for product in combi.product_variant_ids:
                        line_value['product_id'] = product.id
                        print line_value
                        inv_line_id = invoice_line_obj.create(cr, uid, line_value, context=dict(context, no_store_function=True))
                        invoice_line_id.append(inv_line_id)
                invoice_obj.write(cr, uid, invoice_id, {'invoice_line': [(6, 0, invoice_line_id)]}, context=context)
            else:
                invoice_line_id = invoice_line_obj.create(cr, uid, line_value, context=dict(context, no_store_function=True))
                invoice_obj.write(cr, uid, invoice_id, {'invoice_line': [(6, 0, [invoice_line_id])]}, context=context)
            invoice_list.append(invoice_id)

#            invoice_obj.check_bba(cr, uid, invoice_list, context=context)
            wf_service = netsvc.LocalService('workflow')
            wf_service.trg_validate(uid, 'account.invoice', invoice_id, 'invoice_open', cr) 
            cr.commit()

            if membership.interval_type == 'd':
                next_invoice_date = datetime.today() + relativedelta(days=membership.interval_number)
            if membership.interval_type == 'w':
                next_invoice_date = datetime.today() + relativedelta(weeks=membership.interval_number)
            if membership.interval_type == 'm':
                next_invoice_date = datetime.today() + relativedelta(months=membership.interval_number)
            if membership.interval_type == 'y':
                next_invoice_date = datetime.today() + relativedelta(years=membership.interval_number)

            last_invoice_date = datetime.today()

            self.write(cr, uid, membership.id, {'last_invoice_date': last_invoice_date, 'next_invoice_date': next_invoice_date}, context=context)

            membership_line_id = membership_line_obj.create(cr, uid, {
                'partner_id': partner_id,
                'invoice_id': invoice_id,
                'membership_id': membership.id,
                'date_invoice': today,
                'amount_total': amount_inv,
                'product_id': product_id,
            }, context=context) # Don't store function fields inside the loop.

        # Code lifted from orm.py to store function fields outside the loop which
        # is a lot more performant than in every create.
        result = []
        cols = [
            'partner_id',
            'account_id',
            'membership_invoice',
            'fiscal_position',
            'payment_term',
            'sdd_mandate_id',
            'partner_bank_id',
            'reference_type',
            'type',
            'reference',
            'date_due',
            'invoice_line',
        ]
        result += invoice_obj._store_get_values(cr, uid, invoice_list,
            list(set(cols + invoice_obj._inherits.values())),
            context)
        result.sort()
        done = []
        for order, object, some_ids, fields2 in result:
            if not (object, some_ids, fields2) in done:
                self.pool.get(object)._store_set_values(cr, uid, some_ids, fields2, context)
                done.append((object, some_ids, fields2))

        # End of runction field storage. Restart loop, but this time over the invoices instead of partners.
#        for invoice in invoice_obj.browse(cr, uid, invoice_list, context=context):
#            values = {}
#            amount = invoice_obj.action_date_get(cr, uid, [invoice_id], None)
#            if amount:
#                values.update(amount)

    def onchange_product(self, cr, uid, ids, product_id, interval_type, interval_number, context=None):
        res = {}
        if product_id:
            prod_obj = self.pool.get('product.product')
            prod = prod_obj.browse(cr, uid, [product_id])
            list_price = prod.product_tmpl_id.list_price
            if interval_type == 'y' and interval_number and interval_number > 1:
                list_price = list_price * interval_number
            if interval_type == 'm' and interval_number:
                if interval_number < 1 or interval_number > 12:
                    list_price = list_price / 12
                else:
                    list_price = list_price / 12 * interval_number
            if interval_type == 'w' and interval_number:
                if interval_number < 1 or interval_number > 52:
                    list_price = list_price / 52
                else:
                    list_price = list_price / 52 * interval_number
            if interval_type == 'd' and interval_number:
                if interval_number < 1 or interval_number > 365:
                    list_price = list_price / 365
                else:
                    list_price = list_price / 365 * interval_number
            res['membership_amount'] = list_price
        return {'value':res}

    def onchange_invyear(self, cr, uid, ids, nbr_inv_year, context=None):
        res = {}
        if nbr_inv_year:
            interval_type = 'm'
            interval_number = 1
            if nbr_inv_year == '1':
                interval_type = 'y'
                interval_number = 1
            if nbr_inv_year == '2':
                interval_type = 'm'
                interval_number = 6
            if nbr_inv_year == '3':
                interval_type = 'm'
                interval_number = 4
            if nbr_inv_year == '4':
                interval_type = 'm'
                interval_number = '3'
            if nbr_inv_year == '6':
                interval_type = 'm'
                interval_number = '2'
            res['interval_type'] = interval_type
            res['interval_number'] = interval_number
        return {'value':res}

membership_partner_account()

class membership_invoice_line(osv.osv):
    _name = 'membership.invoice.line'

    _columns = {
		'partner_id': fields.many2one('res.partner', 'Partner', select=True),
		'invoice_id': fields.many2one('account.invoice', 'Factuur', select=True),
		'membership_id': fields.many2one('membership.partner.account', 'Lidmaatschap', select=True),
	    'date_invoice': fields.date('Datum Factuur'),
	    'amount_total': fields.float('Bedrag'),
        'product_id': fields.many2one('product.product', 'Product', select=True),
        'invoice_state': fields.related('invoice_id', 'state', type='selection', relation='account.invoice', selection=INVOICE_STATE_SELECTION, string='Factuurstatus'),
    }

    _order = 'date_invoice desc'

membership_invoice_line()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = {
        'membership_invoice': fields.boolean('Lidmaatschapsfactuur'),
        'membership_id': fields.many2one('membership.partner.account', 'Lidmaatschap', select=True),
    }

account_invoice()

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _get_partner_id(self, cr, uid, ids, context=None):
        member_line_obj = self.pool.get('membership.partner.account')
        res_obj =  self.pool.get('res.partner')
        data_inv = member_line_obj.browse(cr, uid, ids, context=context)
        list_partner = []
        for data in data_inv:
            list_partner.append(data.partner_id.id)
        ids2 = list_partner
        while ids2:
            ids2 = res_obj.search(cr, uid, [('associate_member', 'in', ids2)], context=context)
            list_partner += ids2
        return list_partner

    def _get_invoice_partner(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get('account.invoice')
        res_obj = self.pool.get('res.partner')
        data_inv = inv_obj.browse(cr, uid, ids, context=context)
        list_partner = []
        for data in data_inv:
            list_partner.append(data.partner_id.id)
        ids2 = list_partner
        while ids2:
            ids2 = res_obj.search(cr, uid, [('associate_member', 'in', ids2)], context=context)
            list_partner += ids2
        return list_partner

    def _membership_state(self, cr, uid, ids, name, args, context=None):
        """This Function return Membership State For Given Partner.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Partner IDs
        @param name: Field Name
        @param context: A standard dictionary for contextual values
        @param return: Dictionary of Membership state Value
        """
        res = {}
        for id in ids:
            res[id] = 'none'
        today = time.strftime('%Y-%m-%d')
        for id in ids:
            partner_data = self.browse(cr, uid, id, context=context)
            if partner_data.membership_cancel and today > partner_data.membership_cancel:
                res[id] = 'canceled'
                continue
            if partner_data.membership_stop and today > partner_data.membership_stop:
                res[id] = 'old'
                continue
            s = 4
            if partner_data.membership_ids:
                for mline in partner_data.membership_ids:
                    if mline.state:
                        mstate = mline.state
                        if mstate == 'paid':
                            s = 0
                        elif mstate == 'invoiced' and s!=0:
                            s = 1
                        elif mstate == 'canceled' and s!=0 and s!=1:
                            s = 2
                        elif mstate == 'waiting' and s!=0 and s!=1:
                            s = 3
                if s==4:
                    for mline in partner_data.membership_ids:
                        if mline.membership_start < today and mline.membership_end and mline.membership_end < today and mline.membership_start <= mline.membership_end:
                            s = 5
                        else:
                            s = 6
                if s==0:
                    res[id] = 'paid'
                elif s==1:
                    res[id] = 'invoiced'
                elif s==2:
                    res[id] = 'canceled'
                elif s==3:
                    res[id] = 'waiting'
                elif s==5:
                    res[id] = 'old'
                elif s==6:
                    res[id] = 'none'
            if partner_data.free_member and s!=0:
                res[id] = 'free'
            if partner_data.associate_member:
                res_state = self._membership_state(cr, uid, [partner_data.associate_member.id], name, args, context=context)
                res[id] = res_state[partner_data.associate_member.id]
        return res

    def _membership_date(self, cr, uid, ids, name, args, context=None):
        """Return  date of membership"""
        name = name[0]
        res = {}
        member_line_obj = self.pool.get('membership.partner.account')
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.associate_member:
                 partner_id = partner.associate_member.id
            else:
                 partner_id = partner.id
            res[partner.id] = {
                 'membership_start': False,
                 'membership_stop': False,
                 'membership_cancel': False
            }
            if name == 'membership_start':
                line_id = member_line_obj.search(cr, uid, [('partner_id', '=', partner_id)],
                            limit=1, order='membership_start', context=context)
                if line_id:
                        res[partner.id]['membership_start'] = member_line_obj.read(cr, uid, [line_id[0]],
                                ['membership_start'], context=context)[0]['membership_start']

            if name == 'membership_stop':
                line_id1 = member_line_obj.search(cr, uid, [('partner_id', '=', partner_id)],
                            limit=1, order='membership_end desc', context=context)
                if line_id1:
                      res[partner.id]['membership_stop'] = member_line_obj.read(cr, uid, [line_id1[0]],
                                ['membership_end'], context=context)[0]['membership_end']

            if name == 'membership_cancel':
                if partner.membership_state == 'canceled':
                    line_id2 = member_line_obj.search(cr, uid, [('partner_id', '=', partner.id)], limit=1, order='membership_cancel', context=context)
                    if line_id2:
                        res[partner.id]['membership_cancel'] = member_line_obj.read(cr, uid, [line_id2[0]], ['membership_cancel'], context=context)[0]['membership_cancel']
        return res

    def __get_membership_state(self, *args, **kwargs):
        return self._membership_state(*args, **kwargs)

    def _get_partners(self, cr, uid, ids, context=None):
        ids2 = ids
        while ids2:
            ids2 = self.search(cr, uid, [('associate_member', 'in', ids2)], context=context)
            ids += ids2
        return ids

    _columns = {
        'membership_ids': fields.one2many('membership.partner.account', 'partner_id', 'Lidmaatschappen'),
        'membership_line_ids': fields.one2many('membership.invoice.line', 'partner_id', 'Lidmaatschapsfacturen'),
        'membership_state': fields.function(
                    __get_membership_state,
                    string = 'Current Membership Status', type = 'selection',
                    selection = STATE,
                    store = {
                        'account.invoice': (_get_invoice_partner, ['state'], 10),
                        'membership.partner.account': (_get_partner_id, ['state','membership_end', 'membership_cancel', 'membership_start'], 10),
                        'res.partner': (_get_partners, ['free_member', 'membership_state', 'associate_member'], 10)
                    }, help='It indicates the membership state.\n'
                            '-Non Member: A partner who has not applied for any membership.\n'
                            '-Cancelled Member: A member who has cancelled his membership.\n'
                            '-Old Member: A member whose membership date has expired.\n'
                            '-Waiting Member: A member who has applied for the membership and whose invoice is going to be created.\n'
                            '-Invoiced Member: A member whose invoice has been created.\n'
                            '-Paying member: A member who has paid the membership fee.'),
        'membership_start': fields.function(
                    _membership_date, multi = 'membeship_start',
                    string = 'Membership Start Date', type = 'date',
                    store = {
                        'account.invoice': (_get_invoice_partner, ['state'], 10),
                        'membership.partner.account': (_get_partner_id, ['state','membership_end', 'membership_cancel', 'membership_start'], 10, ),
                        'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['free_member'], 10)
                    }, help="Date from which membership becomes active."),
        'membership_stop': fields.function(
                    _membership_date,
                    string = 'Membership End Date', type='date', multi='membership_stop',
                    store = {
                        'account.invoice': (_get_invoice_partner, ['state'], 10),
                        'membership.partner.account': (_get_partner_id, ['state','membership_end', 'membership_cancel', 'membership_start'], 10, ),
                        'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['free_member'], 10)
                    }, help="Date until which membership remains active."),
        'membership_cancel': fields.function(
                    _membership_date,
                    string = 'Cancel Membership Date', type='date', multi='membership_cancel',
                    store = {
                        'account.invoice': (_get_invoice_partner, ['state'], 11),
                        'membership.partner.account': (_get_partner_id, ['state','membership_end', 'membership_cancel', 'membership_start'], 10, ),
                        'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['free_member'], 10)
                    }, help="Date on which membership has been cancelled"),
    }

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
