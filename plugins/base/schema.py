# from flask_rest_jsonapi import Api, ResourceList, ResourceDetail, ResourceRelationship
# from marshmallow_jsonapi.flask import Schema, Relationship
# from marshmallow_jsonapi import fields
# from .tables import Artist, Album, Track
# import server
# import database
#
#
# class ArtistSchema(Schema):
#     class Meta:
#         type_ = 'artist'
#         self_view = 'artist_detail'
#         self_view_kwargs = {'id': '<id>'}
#         self_view_many = 'artist_list'
#
#     id = fields.Integer(dump_only=True)
#
#     name = fields.Str(required=True)
#     name_sort = fields.Str(dump_only=True)
#
#     albums = Relationship(
#         self_view='artist_albums',
#         self_view_kwargs={'id': '<id>'},
#         related_view='artist_list',
#         related_url_kwargs={'id': '<id>'},
#         many=True,
#         schema='AlbumSchema',
#         type_='album'
#     )
#
#
# class ArtistList(ResourceList):
#     schema = ArtistSchema
#     data_layer = {'session': database.db.session, 'model': Artist}
#
#
# class ArtistDetail(ResourceDetail):
#     def before_get_object(self, view_kwargs):
#         if view_kwargs.get('')
#
#     schema = ArtistSchema
#     data_layer = {'session': database.db.session, 'model': Artist}
#
#
# class ArtistRelationship(ResourceRelationship):
#     schema = ArtistSchema
#     data_layer = {'session': database.db.session, 'model': Artist}
#
#
# class AlbumSchema(Schema):
#     class Meta:
#         type_ = 'album'
#         self_view = 'album_detail'
#         self_view_kwargs = {'id': '<id>'}
#         self_view_many = 'album_list'
#
#     id = fields.Integer(dump_only=True)
#
#     name = fields.Str(required=True)
#     name_sort = fields.Str(dump_only=True)
#
#
# class AlbumList(ResourceList):
#     schema = AlbumSchema
#     data_layer = {'session': database.db.session, 'model': Album}
#
#
# class AlbumDetail(ResourceDetail):
#     schema = AlbumSchema
#     data_layer = {'session': database.db.session, 'model': Album}
#
#
# api = Api(server.app)
#
# api.route(ArtistList, 'artist_list', '/artists')
# api.route(ArtistDetail, 'artist_detail', '/artists/<int:id>')
# api.route(ArtistRelationship, 'artist_albums', '/artists/<int:id>/relationships/albums')
# api.route(AlbumList, 'album_list', '/albums', '/artists/<int:id>/albums')
# api.route(AlbumList, 'album_detail', '/albums/<int:id>', '/artists/<int:artist_id>/albums/<int:id>')
