from django.db import models
from student.models import Student

# Create your models here.

class Fee(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=20)
    payment_date = models.DateField()
    STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Paid", "Paid"),
    ("Overdue", "Overdue"),
    ]
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="Pending")
    payment_method = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=40)
    receipt = models.FileField(upload_to='fee_receipt/', blank=True, null=True)

    def __str__(self):
        return self.student.name
    
    def save(self, *args, **kwargs):
        from django.db.models import Sum
        from django.core.files.base import ContentFile
        from .utils import generate_receipt_pdf
        from decimal import Decimal
        import datetime

        # Ensure amount is a Decimal object
        if self.amount is not None:
            self.amount = Decimal(str(self.amount))
        else:
            self.amount = Decimal('0.00')

        # Ensure payment_date is a datetime.date object
        if isinstance(self.payment_date, str):
            try:
                self.payment_date = datetime.datetime.strptime(self.payment_date, '%Y-%m-%d').date()
            except ValueError:
                try:
                    self.payment_date = datetime.datetime.strptime(self.payment_date, '%Y/%m/%d').date()
                except ValueError:
                    self.payment_date = datetime.date.today()

        student = self.student
        
        # Calculate total paid fees (excluding this record if already saved)
        total_paid_query = Fee.objects.filter(student=student, status='Paid')
        if self.pk:
            total_paid_query = total_paid_query.exclude(pk=self.pk)
        total_paid = Decimal(total_paid_query.aggregate(total=Sum('amount'))['total'] or '0.00')
        if self.status == 'Paid':
            total_paid += self.amount
        
        balance_fee = Decimal(student.hostel_fee) - total_paid

        # Generate receipt PDF in memory
        pdf_content = generate_receipt_pdf(self, total_paid, balance_fee)

        # Save PDF to the receipt FileField without triggering a recursive save
        filename = f"receipt_{student.reg_number}_{self.payment_date.strftime('%Y%m%d')}_{self.pk or 'new'}.pdf"
        self.receipt.save(filename, ContentFile(pdf_content), save=False)

        # Save the Fee record to database
        super().save(*args, **kwargs)

        # Send email notification if status is Paid
        if self.status == 'Paid':
            try:
                from django.core.mail import EmailMessage
                from django.conf import settings

                subject = "Fee Payment Update - SEA HSM"
                message = f"Dear {student.name},\n\n" \
                          f"Your fee record has been updated.\n\n" \
                          f"Rs. {self.amount} amount is paid and the balance fee amount is Rs. {balance_fee}.\n\n" \
                          f"Please find your payment receipt attached to this email as a PDF.\n\n" \
                          f"Thank you,\n" \
                          f"SEA Hostel Management System"
                
                email = EmailMessage(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [student.email],
                )
                email.attach(f"Receipt_{student.reg_number}_{self.payment_date.strftime('%Y%m%d')}.pdf", pdf_content, 'application/pdf')
                email.send(fail_silently=True)
            except Exception:
                pass

    

