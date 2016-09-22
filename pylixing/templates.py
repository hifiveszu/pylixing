# -*- coding: utf-8 -*-
from mako.template import Template

from .util import utf8


GET_UPDATE_PRODUCT_INFO = """\
<?xml version="1.0" encoding="UTF-8"?>
<product-code-search-request>
    <update-date-start>{start_date}</update-date-start>
    <update-date-end>{end_date}</update-date-end>
    <start>{start}</start>
    <end>{end}</end>
</product-code-search-request>\
"""

GET_PRODUCT_DETAIL = """\
<?xml version="1.0" encoding="UTF-8"?>
<product-detail-request>
    % if product_code:
    <product-code>{product_code}</product-code>
    % endif
    <currency>{currency}</currency>
</product-detail-request>
"""

SEARCH_PRODUCT = """\
<?xml version="1.0" encoding="UTF-8"?>
<product-search-request>
    % if destination_code:
    <destination-code>${destination_code}</destination-code>
    % endif
    % if product_codes:
        <product-codes>
            % for product_code in product_codes:
                <product-code>${product_code}</product-code>
            % endfor
        </product-codes>
    % endif
    % if tags:
    <tags>
        % for tag in tags:
            <tag>${tag}</tag>
        % endfor
    </tags>
    % endif
    % if keyword:
    <keyword>${keyword}</keyword>
    % endif
    <currency>${currency}</currency>
    % if order_by:
    <order-by>${order_by}</order-by>
    % endif
    % if ascend:
    <ascend>true</ascend>
    % endif
    <start>${start}</start>
    <end>${end}</end>
</product-search-request>
"""

SEARCH_PRODUCT_COUNT = """\
<?xml version="1.0" encoding="UTF-8"?>
<product-search-request>
    % if destination_code:
    <destination-code>${destination_code}</destination-code>
    % endif
    % if product_codes:
        <product-codes>
            % for product_code in product_codes:
                <product-code>${product_code}</product-code>
            % endfor
        </product-codes>
    % endif
    % if tags:
    <tags>
        % for tag in tags:
            <tag>${tag}</tag>
        % endfor
    </tags>
    % endif
    % if keyword:
    <keyword>${keyword}</keyword>
    % endif
    <currency>${currency}</currency>
</product-search-request>
"""

GET_SALE_ITEM_INFO = """\
<?xml version="1.0" encoding="UTF-8"?>
<sale-item-info-request>
    <product-code>{product_code}</product-code>
    <currency>{currency}</currency>
</sale-item-info-request>
"""

GET_SALE_ITEM_DETAIL = """\
<?xml version="1.0" encoding="UTF-8"?>
<sale-item-detail-request>
    <sale-codes>
        % for sale_code in sale_codes:
        <sale-code>${sale_code}</sale-code>
        % endfor
    </sale-codes>
    <currency>${currency}</currency>
</sale-item-detail-request>
"""

GET_PRICE_BY_DAY = """\
<?xml version="1.0" encoding="UTF-8"?>
<price-query-request>
    <sale-code>{sale_code}</sale-code>
    <travel-date>{travel_date}</travel-date>
    <currency>{currency}</currency>
</price-query-request>
"""

GET_PRICE_BY_PERIOD = """\
<?xml version="1.0" encoding="UTF-8"?>
<period-price-query-request>
    <sale-code>{sale_code}</sale-code>
    <product-code>{product_code}</product-code>
    <travel-date>{travel_date}</travel-date>
    <travel-date-end>{travel_date_end}</travel-date-end>
    <currency>{currency}</currency>
</period-price-query-request>
"""

GET_AVAILABLE_DATES = """\
<?xml version="1.0" encoding="UTF-8"?>
<available-dates-request>
    <sale-code>{sale_code}</sale-code>
</available-dates-request>
"""

GET_PICK_OR_DROP = """\
<?xml version="1.0" encoding="UTF-8"?>
<pick-drop-request>
    % if product_codes:
        % for product_code in product_codes:
        <product-codes>
            <product-code>${product_code}</product-code>
        </product-codes>
        % endfor
    % endif
</pick-drop-request>
"""

GET_PRICE_SEGMENT = """\
<?xml version="1.0" encoding="UTF-8"?>
<price-segment-query-request>
    <product-code>{product_code}</product-code>
    <currency>{currency}</currency>
</price-segment-query-request>
"""

GET_AVAILABILITY = """\
<?xml version="1.0" encoding="UTF-8"?>
<availability-request>
    <currency>${currency}</currency>
    <sale-code>${sale_code}</sale-code>
    <travel-date>${travel_date}</travel-date>
    <end-date>${end_date}</end-date>
    % if booked_specifications:
    <booked-specifications>
        % for booked_specification in booked_specifications:
        <booked-specification>
            <specification>${booked_specification['specification']}</specification>
            <num>${booked_specification['num']}</num>
        </booked-specification>
        % endfor
    </booked-specifications>
    % endif
    % if booked_additional_options:
    <booked-additional-options>
        % for additional_option in booked_additional_options:
        <additional-option>
            <option-code>${additional_option['option_code']}</option-code>
            <num>${additional_option['num']}</num>
        </additional-option>
        % endfor
    </booked-additional-options>
    % endif
</availability-request>
"""

GET_BOOK_LIMITS = """\
<?xml version="1.0" encoding="UTF-8"?>
<book-limits-request>
    % if sale_codes:
    <sale-codes>
        % for sale_code in sale_codes:
        <sale-code>${sale_code}</sale-code>
        % endfor
    </sale-codes>
    % endif
</book-limits-request>
"""

BOOK = """\
<?xml version="1.0" encoding="UTF-8"?>
<book_request>
    <distributor-order-refer>${distributor_order_refer}</distributor-order-refer>
    % if currency:
    <currency>${currency}</currency>
    % endif
    <booker-name>${booker_name}</booker-name>
    <booker-email>${booker_email}</booker-email>
    <booker-phone>${booker_phone}</booker-phone>
    % if callback_url:
    <callback-url>${callback_url}</callback-url>
    % endif
    % if items:
    <items>
        % for book_item in items:
        <book-item>
            <email>${book_item['email']}</email>
            <distributor-order-item-refer>
                ${book_item['distributor_order_item_refer']}
            </distributor-order-item-refer>
            % if book_item.get('pickup_code'):
            <pickup-code>${book_item['pickup_code']}</pickup-code>
            % endif
            % if book_item.get('pickup_point'):
            <pickup-point>${book_item['pickup_point']}</pickup-point>
            % endif
            % if book_item.get('dropoff_code'):
            <dropoff-code>${book_item['dropoff_code']}</dropoff-code>
            % endif
            % if book_item.get('dropoff_point'):
            <dropoff-point>${dropoff_point}</dropoff-point>
            % endif
            <travel-date>${book_item['travel_date']}</travel-date>
            <product-code>${book_item['product_code']}</product-code>
            <sale-code>${book_item['sale_code']}</sale-code>
            % if book_item.get('special_requirements'):
            <special-requirements>${book_item['special_requirements']}</special-requirements>
            % endif
            % if book_item.get('book_questions'):
            <book-questions>
                % for book_question in book_item['book_questions']:
                <book-question>
                    <question-id>${book_question['question_id']}</question-id>
                    <answer>${book_question['answer']}</answer>
                </book-question>
                % endfor
            </book-questions>
            % endif
            % if book_item.get('booked_specifications'):
            <booked-specifications>
                % for booked_specification in book_item['booked_specifications']:
                <booked-specification>
                    <specification>${booked_specification['specification_id']}</specification>
                    <num>${booked_specification['num']}</num>
                </booked-specification>
                % endfor
            </booked-specifications>
            % endif
            % if book_item.get('leader'):
            <leader>
                <phone>${book_item['leader'].get('phone')}</phone>
                <crowd-type>${book_item['leader'].get('crowd_type', '')}</crowd-type>
                <firstname>${book_item['leader'].get('firstname')}</firstname>
                <surname>${book_item['leader'].get('surname')}</surname>
                % if book_item['leader'].get('gender'):
                    <gender>${book_item['leader'].get('gender')}</gender>
                % endif
                % if book_item['leader'].get('nationality_code'):
                    <nationality-code>${book_item['leader'].get('nationality_code')}</nationality-code>
                % endif
                % if book_item['leader'].get('birth'):
                    <birth>${book_item['leader'].get('birth')}</birth>
                % endif
                % if book_item['leader'].get('identity_type'):
                    <identity-type>${book_item['leader'].get('identity_type')}</identity-type>
                % endif
                % if book_item['leader'].get('identity_num'):
                    <identity-num>${book_item['leader'].get('identity_num')}</identity-num>
                % endif
                % if book_item['leader'].get('identity_expire_date'):
                    <identity-expire-date>${book_item['leader'].get('identity_expire_date')}</identity-expire-date>
                % endif
                % if book_item['leader'].get('specifications'):
                <specifications>
                    % for specification_id in book_item['leader']['specifications']:
                    <specification>${specification_id}</specification>
                    % endfor
                </specifications>
                % endif
            </leader>
            % endif
            % if book_item.get('travellers'):
            <travellers>
                % for traveller in book_item['travellers']:
                <traveller>
                    <crowd-type>${traveller.get('crowd_type', '')}</crowd-type>
                    <firstname>${traveller.get('firstname')}</firstname>
                    <surname>${traveller.get('surname')}</surname>
                    % if traveller.get('gender'):
                        <gender>${traveller.get('gender')}</gender>
                    % endif
                    % if traveller.get('nationality_code'):
                        <nationality-code>${traveller.get('nationality_code')}</nationality-code>
                    % endif
                    % if traveller.get('birth'):
                        <birth>${traveller.get('birth')}</birth>
                    % endif
                    % if traveller.get('identity_type'):
                        <identity-type>${traveller.get('identity_type')}</identity-type>
                    % endif
                    % if traveller.get('identity_num'):
                        <identity-num>${traveller.get('identity_num')}</identity-num>
                    % endif
                    % if traveller.get('identity_expire_date'):
                        <identity-expire-date>${traveller.get('identity_expire_date')}</identity-expire-date>
                    % endif
                    % if traveller.get('specifications'):
                    <specifications>
                        % for specification_id in traveller['specifications']:
                        <specification>
                            ${specification_id}
                        </specification>
                        % endfor
                    </specifications>
                    % endif
                </traveller>
                % endfor
            </travellers>
            % endif
            % if book_item.get('booked_options'):
            <booked-options>
                % for booked_option in book_item['booked_options']:
                <additional-option>
                    <option-code>${booked_option['option_code']}</option-code>
                    <num>${booked_option['num']}</num>
                </additional-option>
                % endfor
            </booked-options>
            % endif
            % if book_item.get('delivery'):
            <delivery>
                <mode>${book_item['delivery'].get('mode')}</mode>
                <receiver>${book_item['delivery'].get('receiver')}</receiver>
                <phone>${book_item['delivery'].get('phone')}</phone>
                <address>${book_item['delivery'].get('address')}</address>
                <postcode>${book_item['delivery'].get('postcode')}</postcode>
                <need-invoice>${book_item['delivery'].get('need_invoice')}</need-invoice>
                <invoice-info>${book_item['delivery'].get('invoice_info')}</invoice-info>
            </delivery>
            % endif
        </book-item>
        % endfor
    </items>
    % endif
</book_request>
"""


GET_ORDER_STATUS = """\
<?xml version="1.0" encoding="UTF-8"?>
<order-request>
    <order-cds>
    % for order_cd in order_cds:
        <order-cd>${order_cd}</order-cd>
    % endfor
    </order-cds>
    <ref-order-cds>
    % for ref_order_cd in ref_order_cds:
        <ref-order-cd>${ref_order_cd}</ref-order-cd>
    % endfor
    </ref-order-cds>
</order-request>
"""

CONFIRM = """\
<?xml version="1.0" encoding="UTF-8"?>
<confirm-request>
    <order-cd>${order_cd}</order-cd>
</confirm-request>
"""

REFUND = """\
<?xml version="1.0" encoding="UTF-8"?>
<refund-request>
    <order-cd>${order_cd}</order-cd>
    <order-item-cd>${order_item_cd}</order-item-cd>
    <refund-reason>${refund_reason}</refund-reason>
</refund-request>
"""


class _Template(object):
    def __init__(self, text, use_mako=False):
        # print text
        if use_mako:
            self.render_func = Template(text).render
        else:
            self.render_func = text.format

    def render(self, *args, **kwargs):

        context = dict(*args, **kwargs)
        # print context
        return self.render_func(**context)


_template_store = {
    'getUpdateProductInfo': _Template(GET_UPDATE_PRODUCT_INFO, use_mako=False),
    'getProductDetail': _Template(GET_PRODUCT_DETAIL, use_mako=False),
    'searchProduct': _Template(SEARCH_PRODUCT, use_mako=True),
    'searchProductCount': _Template(SEARCH_PRODUCT_COUNT, use_mako=True),
    'getSaleItemInfo': _Template(GET_SALE_ITEM_INFO, use_mako=False),
    'getSaleItemDetail': _Template(GET_SALE_ITEM_DETAIL, use_mako=True),
    'getPriceByDay': _Template(GET_PRICE_BY_DAY, use_mako=False),
    'getPriceByPeriod': _Template(GET_PRICE_BY_PERIOD, use_mako=False),
    'getAvailableDates': _Template(GET_AVAILABLE_DATES, use_mako=False),
    'getPickOrDrop': _Template(GET_PICK_OR_DROP, use_mako=True),
    'getPriceSegment': _Template(GET_PRICE_SEGMENT, use_mako=False),
    'getAvailablity': _Template(GET_AVAILABILITY, use_mako=True),
    'getBookLimits': _Template(GET_BOOK_LIMITS, use_mako=True),
    'book': _Template(BOOK, use_mako=True),
    'getOrderStatus': _Template(GET_ORDER_STATUS, use_mako=True),
    'refund': _Template(REFUND, use_mako=True),
    'confirm': _Template(CONFIRM, use_mako=True),
}


def render(method, **context):
    template = _template_store.get(method)
    if not template:
        return ''
    return utf8(template.render(**context))
