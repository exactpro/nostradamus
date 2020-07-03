from mongoengine import (
    DynamicDocument,
    StringField,
    IntField,
    ListField,
    EmbeddedDocumentField,
    DateTimeField,
    EmbeddedDocument,
)


class Item(EmbeddedDocument):
    Field = StringField()
    From = StringField()
    To = StringField()


class History(EmbeddedDocument):
    Author = StringField(required=True)
    Created = DateTimeField(required=True)
    Items = ListField(EmbeddedDocumentField(Item))


class Bug(DynamicDocument):
    Project = StringField(required=True)
    Attachments = IntField()
    Priority = StringField(required=True)
    Created = DateTimeField(required=True, null=True)
    Resolved = DateTimeField(null=True)
    Updated = DateTimeField(null=True)
    Labels = StringField()
    Comments = IntField()
    Status = StringField(required=True)
    Key = StringField(required=True, unique=True)
    Summary = StringField(required=True)
    Resolution = StringField(required=True)
    Description = StringField(required=True)
    Description_tr = StringField(required=True)
    ttr = IntField()
    Markup = IntField()
    Components = StringField()
    Version = StringField()
    Assignee = StringField()
    Reporter = StringField(required=True)

    History = ListField(EmbeddedDocumentField(History))
