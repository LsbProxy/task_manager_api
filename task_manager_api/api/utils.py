TASK_STATUS_CHOICES = [
    ('TD', 'TODO'),
    ('IP', 'IN PROGRESS'),
    ('WA', 'WAITING'),
    ('DN', 'DONE'),
    ('DU', 'DUPLICATE'),
]


def remove_list_serializer_fields(self, fields, **kwargs):
    try:
        # modify fields if the serializer is being invoked by another serializer or the action is list
        modify_fields = kwargs.get(
            'source') or kwargs['context']['view'].action == 'list'

        if modify_fields:
            for field in fields:
                self.fields.pop(field)
    except Exception:
        return
