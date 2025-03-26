from django.db import models
from publishers.models import Publisher
from authors.models import Author
from django.utils.text import slugify
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class BookTitle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Book position: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    

class Book(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=24, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.book_id:
            self.book_id = str(uuid.uuid4()).replace('_', '')[:24].lower()
    
    # تولید QR کد
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
    )
        qr.add_data(self.book_id)
        qr.make(fit=True)

        qrcode_img = qr.make_image(fill='black', back_color='white')

        # تبدیل تصویر QRCode به فرمت مناسب PIL
        qr_pil = qrcode_img.convert("RGB")  

        # ایجاد یک canvas هم‌اندازه با تصویر QR
        canvas = Image.new('RGB', qr_pil.size, 'white')
        
        # چسباندن تصویر QR در موقعیت (0,0)
        canvas.paste(qr_pil, (0, 0))  

        fname = f'qr_code-{self.title}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        
        # اصلاح این خط (sef -> self)
        self.qr_code.save(fname, File(buffer), save=False)

        canvas.close()
        
        super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     if not self.book_id:
    #         self.book_id = str(uuid.uuid4()).replace('_', '')[:24].lower()
            
    #     qrcode_img = qrcode.make(self.book_id)
    #     canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
    #     canvas.paste(qrcode_img)
    #     fname = f'qr_code-{self.title}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer, 'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
        
    #     super().save(*args, **kwargs)