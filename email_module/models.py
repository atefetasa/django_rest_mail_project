from django.db import models
from account_module.models import User, Contact, Signature
from .validators import validate_file_size
from ckeditor.fields import RichTextField


class Label(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')
    label_name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = 'label'
        verbose_name_plural = 'labels'

    def __str__(self):
        return self.label_name


class Email(models.Model):
    title = models.CharField(max_length=500, verbose_name='email title', null=True, blank=True)
    text = RichTextField(null=True, blank=True)
    file = models.FileField(upload_to='attached_files', null=True, blank=True, validators=[validate_file_size])
    sender = models.ForeignKey(User, on_delete=models.SET('deleted_account'), related_name='sent_Emails')
    draft = models.BooleanField(default=False)
    direct_receivers = models.ManyToManyField(User, blank=True, related_name='direct_receivers')
    cc_receivers = models.ManyToManyField(User, blank=True, related_name='cc_receivers')
    bcc_receivers = models.ManyToManyField(User, blank=True, related_name='bcc_receivers')
    replied_email = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    deleted_by_user = models.ManyToManyField(User, blank=True, related_name='is_deleted_by_user')
    labels = models.ManyToManyField(Label, blank=True, related_name='email_labels', verbose_name='email_labels')
    signature = models.ForeignKey(Signature, on_delete=models.SET_NULL, null=True, blank=True)
    read_by_user = models.ManyToManyField(User, blank=True, related_name='is_read_by_user')
    archived_by_user = models.ManyToManyField(User, blank=True, related_name='is_archived_by_user')

    @property
    def file_size(self):
        if self.file and hasattr(self.file, 'size'):
            return self.file.size

    class Meta:
        verbose_name = 'email'
        verbose_name_plural = 'emails'

    def __str__(self):
        return self.title, self.text, self.direct_receivers, self.cc_receivers, self.bcc_receivers


