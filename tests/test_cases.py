# tests/test_cases.py

pub_test_cases = [
    {   # publish to queue 1
        'payload': {
            'pub_module_name': 'module1',
            'topic': 'queue1',
            'message_body': {"key": "test value"},
        },
        'message': 'Queue entry published.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': False,
            'pub_module_name': 'module1',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,   # always false
            'authentication_key': False,    # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {   # publish to queue 2
        'payload': {
            'pub_module_name': 'module1',
            'topic': 'queue2',
            'message_body': {"key": "test value"},
        },
        'message': 'Queue entry published.',
        'status_code': 200,
        'return': {
            'topic': 'queue2',
            'has_authentication': False,
            'pub_module_name': 'module1',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {   # publish to queue 1 with authentication
        'payload': {
            'pub_module_name': 'module1',
            'topic': 'queue1',
            'message_body': {"key": "test value"},
            'authentication_key': 'e49a307c-5f5b-4857-bb95-9f56368f91e6',
        },
        'message': 'Queue entry published.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': True,
            'pub_module_name': 'module1',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # publish to queue 1 with authentication
        'payload': {
            'pub_module_name': 'module1',
            'topic': 'queue1',
            'message_body': {"key": "test value"},
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
        },
        'message': 'Queue entry published.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': True,
            'pub_module_name': 'module1',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # publish to queue 1 with authentication target module4
        'payload': {
            'pub_module_name': 'module1',
            'topic': 'queue1',
            'message_body': {"key": "test value"},
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
            'target_module_name': 'module4'
        },
        'message': 'Queue entry published.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': True,
            'pub_module_name': 'module1',
            'target_module_name': 'module4',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': True,
            'received_at': True,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # publish to queue 1 target module4
        'payload': {
            'pub_module_name': 'module1',
            'topic': 'queue1',
            'message_body': {"key": "test value"},
            'target_module_name': 'module4'
        },
        'message': 'Queue entry published.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': False,
            'pub_module_name': 'module1',
            'target_module_name': 'module4',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': True,
            'received_at': True,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
]

# #############################################################################
sub_test_cases = [
    {   # sub to queue 2
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue2',
        },
        'message': 'Message available.',
        'status_code': 200,
        'return': {
            'topic': 'queue2',
            'has_authentication': False,
            'pub_module_name': 'module1',
            'delivered_to_module': 'module3',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,   # always false
            'authentication_key': False,    # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': True,
            'schedule_date': False,
            'delivered_to_module': True,
        }
    },
    {  # sub to queue 2 again, expect nothing
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue2',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # sub to queue 1 - No auth
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue1',
        },
        'message': 'Message available.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': False,
            'pub_module_name': 'module1',
            'delivered_to_module': 'module3',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': True,
            'schedule_date': False,
            'delivered_to_module': True,
        }
    },
    {  # sub to queue 1 again, no auth, expect nothing
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue1',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # sub to queue 1 - with auth
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue1',
            'authentication_key': 'e49a307c-5f5b-4857-bb95-9f56368f91e6',
        },
        'message': 'Message available.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': True,
            'pub_module_name': 'module1',
            'delivered_to_module': 'module3',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': True,
            'schedule_date': False,
            'delivered_to_module': True,
        }
    },
    {  # sub to queue 1 again, auth, expect nothing
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue1',
            'authentication_key': 'e49a307c-5f5b-4857-bb95-9f56368f91e6',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # sub to queue 1 - with auth new key
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue1',
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
        },
        'message': 'Message available.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': True,
            'pub_module_name': 'module1',
            'delivered_to_module': 'module3',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': False,
            'received_at': True,
            'delivered_at': True,
            'schedule_date': False,
            'delivered_to_module': True,
        }
    },
    {  # sub to queue 1 again, auth, expect nothing
        'payload': {
            'sub_module_name': 'module3',
            'topic': 'queue1',
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # sub to queue 1 as module 4 - no auth
        'payload': {
            'sub_module_name': 'module4',
            'topic': 'queue1',
        },
        'message': 'Message available.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': False,
            'pub_module_name': 'module1',
            'target_module_name': 'module4',
            'delivered_to_module': 'module4',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': True,
            'received_at': True,
            'delivered_at': True,
            'schedule_date': False,
            'delivered_to_module': True,
        }
    },
    {  # sub as module 4 to queue 1 again, no auth, expect nothing
        'payload': {
            'sub_module_name': 'module4',
            'topic': 'queue1',
            # 'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # sub as module 4 to queue 1 again, wrong auth, expect nothing
        'payload': {
            'sub_module_name': 'module4',
            'topic': 'queue1',
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b99',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
    {  # sub to queue 1 as module 4 -  auth
        'payload': {
            'sub_module_name': 'module4',
            'topic': 'queue1',
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
        },
        'message': 'Message available.',
        'status_code': 200,
        'return': {
            'topic': 'queue1',
            'has_authentication': True,
            'pub_module_name': 'module1',
            'target_module_name': 'module4',
            'delivered_to_module': 'module4',
        },
        "fields_exist": {
            'id': True,
            'pub_module_name': True,
            'topic': True,
            'message_body': True,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': True,
            'target_module_name': True,
            'received_at': True,
            'delivered_at': True,
            'schedule_date': False,
            'delivered_to_module': True,
        }
    },
    {  # sub as module 4 to queue 1 again, auth, expect nothing
        'payload': {
            'sub_module_name': 'module4',
            'topic': 'queue1',
            'authentication_key': 'f917d8a4-7e97-4c3a-9077-4e8a8f3a5b98',
        },
        'detail': 'No messages.',
        'status_code': 404,
        'return': {},
        "fields_exist": {
            'id': False,
            'pub_module_name': False,
            'topic': False,
            'message_body': False,
            '_authentication_key': False,  # always false
            'authentication_key': False,  # always false
            'has_authentication': False,
            'target_module_name': False,
            'received_at': False,
            'delivered_at': False,
            'schedule_date': False,
            'delivered_to_module': False,
        }
    },
]

# # #############################################################################
# pub_test_cases_time = [
#     {   # publish to queue 1
#         'payload': {
#             'pub_module_name': 'module1',
#             'topic': 'queue1',
#             'message_body': {"key": "test value"},
#         },
#         'message': 'Queue entry published.',
#         'sleep': 1,
#         'status_code': 200,
#         'return': {
#             'topic': 'queue1',
#             'has_authentication': False,
#             'pub_module_name': 'module1',
#         },
#         "fields_exist": {
#             'id': True,
#             'pub_module_name': True,
#             'topic': True,
#             'message_body': True,
#             '_authentication_key': False,   # always false
#             'authentication_key': False,    # always false
#             'has_authentication': True,
#             'target_module_name': False,
#             'received_at': True,
#             'delivered_at': False,
#             'schedule_date': True,
#             'delivered_to_module': False,
#         }
#     },
# ]
#
# # #############################################################################
# sub_test_cases_time = [
#     {  # sub to queue 1 , expect nothing
#         'payload': {
#             'sub_module_name': 'module4',
#             'topic': 'queue1',
#         },
#         'detail': 'No messages.',
#         'status_code': 404,
#         'return': {},
#         "fields_exist": {
#             'id': False,
#             'pub_module_name': False,
#             'topic': False,
#             'message_body': False,
#             '_authentication_key': False,  # always false
#             'authentication_key': False,  # always false
#             'has_authentication': False,
#             'target_module_name': False,
#             'received_at': False,
#             'delivered_at': False,
#             'schedule_date': False,
#             'delivered_to_module': False,
#         }
#     },
#     {  # sub to queue 1
#         'payload': {
#             'sub_module_name': 'module3',
#             'topic': 'queue1',
#         },
#         'sleep': 2,
#         'message': 'Message available.',
#         'status_code': 200,
#         'return': {
#             'topic': 'queue1',
#             'pub_module_name': 'module1',
#             'delivered_to_module': 'module3',
#         },
#         "fields_exist": {
#             'id': True,
#             'pub_module_name': True,
#             'topic': True,
#             'message_body': True,
#             '_authentication_key': False,  # always false
#             'authentication_key': False,  # always false
#             'has_authentication': False,
#             'target_module_name': False,
#             'received_at': True,
#             'delivered_at': True,
#             'schedule_date': True,
#             'delivered_to_module': True,
#         }
#     },
# ]

# end
