# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Meeting.vote_until'
        db.add_column(u'meetings_meeting', 'vote_until',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Meeting.vote_until'
        db.delete_column(u'meetings_meeting', 'vote_until')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'communities.community': {
            'Meta': {'object_name': 'Community'},
            'board_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'has_issue_votes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'official_identifier': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'b4lwv3fq4ozzhyzcs2l1y5cv'", 'unique': 'True', 'max_length': '24'}),
            'upcoming_meeting_comments': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_guests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upcoming_meeting_location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': u"orm['users.OCUser']"}),
            'upcoming_meeting_published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upcoming_meeting_summary': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'upcoming_meeting_version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'issues.issue': {
            'Meta': {'object_name': 'Issue'},
            'abstract': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'calculated_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': u"orm['communities.Community']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('ocd.base_models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues_created'", 'to': u"orm['users.OCUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length_in_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_in_upcoming_meeting': ('django.db.models.fields.IntegerField', [], {'default': '9999', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'qcwvzd0jt0n5uit44zq84orp'", 'unique': 'True', 'max_length': '24'})
        },
        u'meetings.agendaitem': {
            'Meta': {'unique_together': "(('meeting', 'issue'),)", 'object_name': 'AgendaItem'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Issue']"}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agenda'", 'to': u"orm['meetings.Meeting']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
        },
        u'meetings.meeting': {
            'Meta': {'ordering': "('-held_at',)", 'object_name': 'Meeting'},
            'agenda_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['issues.Issue']", 'symmetrical': 'False', 'through': u"orm['meetings.AgendaItem']", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings'", 'to': u"orm['communities.Community']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings_created'", 'to': u"orm['users.OCUser']"}),
            'guests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'held_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participated_in_meeting'", 'symmetrical': 'False', 'through': u"orm['meetings.MeetingParticipant']", 'to': u"orm['users.OCUser']"}),
            'scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'u548etsmg743py55luwz7fkh'", 'unique': 'True', 'max_length': '24'}),
            'vote_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'meetings.meetingexternalparticipant': {
            'Meta': {'object_name': 'MeetingExternalParticipant'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetings.Meeting']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'meetings.meetingparticipant': {
            'Meta': {'unique_together': "(('meeting', 'ordinal'), ('meeting', 'user'))", 'object_name': 'MeetingParticipant'},
            'default_group_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['meetings.Meeting']"}),
            'ordinal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['users.OCUser']"})
        },
        u'users.ocuser': {
            'Meta': {'object_name': 'OCUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['meetings']