# coding: utf8
import datetime
import mongoengine


class MBookingLog(mongoengine.Document):
    meta = {"collection": "booking_log"}
    booking_id = mongoengine.IntField(required=True)
    store_id = mongoengine.IntField(required=True)
    is_confirm = mongoengine.IntField(required=False, default=1)
    is_sent_confirm = mongoengine.IntField(required=False, default=1)
    is_sent_result = mongoengine.IntField(required=False, default=1)
    check_code = mongoengine.StringField(required=False)
    active_code = mongoengine.ListField(required=False)
    hold_code = mongoengine.ListField(required=False)
    unhold_code = mongoengine.ListField(required=False)
    is_active = mongoengine.IntField(required=False, default=1)
    created_time = mongoengine.DateField(required=False, default=datetime.datetime.now)
    updated_time = mongoengine.DateField(required=False, default=datetime.datetime.now)
