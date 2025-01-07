from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from rest_framework.response import Response

from api.serializers import ContactSerializer
from law.forms import ContactsViewModelForm
from law.models import Contact

from rest_framework.decorators import api_view

# Örnek blog verileri (gerçek uygulamada veritabanından gelecek)
BLOG_POSTS = [
    {
        'title': 'Kira Sözleşmesinde Dikkat Edilmesi Gerekenler',
        'slug': 'kira-sozlesmesinde-dikkat-edilmesi-gerekenler',
        'category': 'Gayrimenkul Hukuku',
        'date': '30 Aralık 2024',
        'content': '''Kira sözleşmesi imzalarken dikkat edilmesi gereken önemli noktalar ve yasal haklarınız hakkında detaylı bilgilendirme. 
                   Kiracı ve ev sahibi olarak haklarınızı öğrenin, yasal süreçler hakkında bilgi edinin.
                   
                   1. Sözleşme İçeriği
                   2. Yasal Yükümlülükler
                   3. Depozito ve Ödemeler
                   4. Fesih Şartları
                   5. Ortak Alanlar
                   ''',
        'author_name': 'Av. Gülşah Aybike Öztaylan',
        'author_title': 'Kurucu Ortak',
        'author_image': 'https://source.unsplash.com/400x400/?lawyer,woman',
        'tags': ['Kira Hukuku', 'Gayrimenkul', 'Sözleşmeler']
    },
    {
        'title': 'İş Kazalarında İşçi ve İşveren Hakları',
        'slug': 'is-kazalarinda-isci-ve-isveren-haklari',
        'category': 'İş Hukuku',
        'date': '28 Aralık 2024',
        'content': '''İş kazası durumunda tarafların hak ve sorumlulukları, yasal süreç ve tazminat hakları konusunda kapsamlı rehber.
                   
                   • İş Kazası Tanımı
                   • İşverenin Yükümlülükleri
                   • İşçinin Hakları
                   • Tazminat Hesaplama
                   • Dava Süreçleri
                   ''',
        'author_name': 'Av. Gülşah Aybike Öztaylan',
        'author_title': 'Kurucu Ortak',
        'author_image': 'https://source.unsplash.com/400x400/?lawyer,woman',
        'tags': ['İş Hukuku', 'İş Kazası', 'İşçi Hakları']
    },
    {
        'title': '2024 Yılı İş Hukuku Mevzuat Değişiklikleri',
        'slug': '2024-yili-is-hukuku-mevzuat-degisiklikleri',
        'category': 'Mevzuat Değişiklikleri',
        'date': '25 Aralık 2024',
        'content': '''2024 yılında iş hukuku alanında yapılan önemli değişiklikler ve uygulamaya yansımaları hakkında detaylı bilgilendirme.

                   1. Asgari Ücret Düzenlemeleri
                   • 2024 yılı asgari ücret tutarı
                   • Vergi muafiyetleri ve kesintiler
                   • İşverenlere sağlanan teşvikler
                   
                   2. Kıdem Tazminatı Tavanı
                   • Yeni tavan tutarı
                   • Hesaplama yöntemi değişiklikleri
                   • Uygulama örnekleri
                   
                   3. Uzaktan Çalışma Düzenlemeleri
                   • Yeni yasal çerçeve
                   • İşveren yükümlülükleri
                   • Çalışan hakları
                   
                   4. İş Güvenliği Mevzuatı
                   • Güncellenen yönetmelikler
                   • Yeni güvenlik standartları
                   • Denetim kriterleri
                   
                   5. Sosyal Güvenlik Primleri
                   • Prim oranlarındaki değişiklikler
                   • Teşvik sistemindeki yenilikler
                   • Başvuru süreçleri
                   
                   Bu değişikliklerin işçi ve işverenlere etkileri, uyum süreçleri ve dikkat edilmesi gereken hususlar makalemizde detaylı olarak ele alınmıştır.
                   ''',
        'author_name': 'Av. Gülşah Aybike Öztaylan',
        'author_title': 'Kurucu Ortak',
        'author_image': 'https://source.unsplash.com/400x400/?lawyer,woman',
        'tags': ['Mevzuat', 'İş Hukuku', 'Asgari Ücret', 'Kıdem Tazminatı', 'İş Güvenliği']
    }
]

# Örnek başarı hikayeleri
SUCCESS_STORIES = [
    {
        'category': 'İş Hukuku',
        'title': 'Haksız İşten Çıkarma Davası',
        'description': '''İşveren tarafından haksız nedenlerle işten çıkarılan müvekkilimizin haklarını başarıyla savunduk. 
                      Kıdem ve ihbar tazminatlarının yanı sıra, işe iade kararı alındı.''',
        'result': 'Dava müvekkil lehine sonuçlandı',
        'year': '2023',
        'duration': '8 ay',
        'icon': 'fa-gavel'
    },
    {
        'category': 'Gayrimenkul Hukuku',
        'title': 'Kat Mülkiyeti Uyuşmazlığı',
        'description': '''Site yönetimi ile yaşanan hukuki uyuşmazlıkta, müvekkilimizin haklarını koruyarak 
                      ortak alanların kullanımı konusunda emsal niteliğinde bir karar elde ettik.''',
        'result': 'Anlaşma ile sonuçlandı',
        'year': '2023',
        'duration': '6 ay',
        'icon': 'fa-building'
    },
    {
        'category': 'Ticaret Hukuku',
        'title': 'Şirket Birleşmesi Süreci',
        'description': '''İki büyük ölçekli şirketin birleşme sürecinde hukuki danışmanlık sağladık. 
                      Tüm yasal süreçler başarıyla tamamlandı.''',
        'result': 'Başarıyla tamamlandı',
        'year': '2024',
        'duration': '12 ay',
        'icon': 'fa-handshake'
    }
]

# Sıkça Sorulan Sorular verileri
FAQ_ITEMS = [
    {
        'category': 'Genel Sorular',
        'questions': [
            {
                'question': 'Avukatlık ücretleri nasıl belirlenir?',
                'answer': '''Avukatlık ücretleri, davanın türü, karmaşıklığı ve süresine göre belirlenir. 
                         Ücretler, Türkiye Barolar Birliği'nin belirlediği asgari ücret tarifesinin altında olmamak 
                         kaydıyla, yapılacak iş ve hizmetin kapsamına göre karşılıklı anlaşma ile belirlenir.'''
            },
            {
                'question': 'İlk görüşme ücretli midir?',
                'answer': '''İlk tanışma ve ön değerlendirme görüşmemiz ücretsizdir. Bu görüşmede hukuki 
                         sorununuzu dinler, izlenecek yol haritasını belirler ve tahmini maliyet 
                         bilgisi veririz.'''
            }
        ]
    },
    {
        'category': 'Dava Süreci',
        'questions': [
            {
                'question': 'Dava açmak için hangi belgeler gerekir?',
                'answer': '''Gerekli belgeler davanın türüne göre değişmekle birlikte, genel olarak:
                         • Kimlik fotokopisi
                         • Dava konusuyla ilgili tüm yazışmalar
                         • Delil niteliğindeki belgeler
                         • Varsa tanık bilgileri
                         gerekmektedir. Detaylı bilgi için bizimle iletişime geçebilirsiniz.'''
            },
            {
                'question': 'Dava süreci ortalama ne kadar sürer?',
                'answer': '''Dava süreleri, davanın türüne ve karmaşıklığına göre değişkenlik gösterir. 
                         Basit bir iş davası 6-12 ay sürebilirken, karmaşık ticari davalar 
                         2-3 yıla kadar uzayabilmektedir.'''
            }
        ]
    },
    {
        'category': 'Ücretlendirme',
        'questions': [
            {
                'question': 'Ödeme seçenekleri nelerdir?',
                'answer': '''Ücret ödemeleri dava türüne göre farklılık gösterir:
                         • Sabit ücret
                         • Taksitli ödeme
                         • Sonuç odaklı ücretlendirme
                         seçenekleri mevcuttur. Her müvekkilimizin bütçesine uygun bir ödeme planı oluşturuyoruz.'''
            },
            {
                'question': 'Dava kazanılmazsa ücret iadesi yapılır mı?',
                'answer': '''Avukatlık ücretleri, sonuçtan bağımsız olarak verilen hizmet karşılığıdır. 
                         Ancak bazı dava türlerinde "başarı primi" şeklinde ek ücretlendirme yapılabilir.'''
            }
        ]
    },
    {
        'category': 'Randevu ve İletişim',
        'questions': [
            {
                'question': 'Randevu almak için ne yapmam gerekiyor?',
                'answer': '''Randevu almak için:
                         • Telefon ile arayabilir
                         • Web sitemizdeki iletişim formunu doldurabilir
                         • E-posta gönderebilirsiniz
                         En kısa sürede size dönüş yapılacaktır.'''
            },
            {
                'question': 'Acil durumlarda nasıl ulaşabilirim?',
                'answer': '''Mesai saatleri dışında acil durumlar için 7/24 ulaşabileceğiniz acil durum 
                         hattımız mevcuttur. Ayrıca mobil uygulamamız üzerinden de anlık mesaj gönderebilirsiniz.'''
            }
        ]
    }
]

def blog_list(request):
    # Kategori filtresi
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    
    # Filtreleme
    posts = BLOG_POSTS
    if category:
        # Kategori adını URL-friendly formattan normal formata çevir
        category_map = {
            'is-hukuku': 'İş Hukuku',
            'gayrimenkul-hukuku': 'Gayrimenkul Hukuku',
            'ticaret-hukuku': 'Ticaret Hukuku',
            'aile-hukuku': 'Aile Hukuku',
            'mevzuat-degisiklikleri': 'Mevzuat Değişiklikleri'
        }
        display_category = category_map.get(category)
        if display_category:
            posts = [post for post in posts if post['category'] == display_category]
    
    if tag:
        posts = [post for post in posts if tag in post['tags']]
    
    # Sayfalama
    paginator = Paginator(posts, 6)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'current_category': category,  # Aktif kategoriyi template'e gönder
    }
    return render(request, 'law/blog_list.html', context)

def blog_detail(request, slug):
    # Post'u bul
    post = next((post for post in BLOG_POSTS if post['slug'] == slug), None)
    if not post:
        raise Http404("Makale bulunamadı")
    
    # Benzer yazıları bul (aynı kategoriden)
    related_posts = [p for p in BLOG_POSTS 
                    if p['category'] == post['category'] and p['slug'] != slug][:3]
    
    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'law/blog_detail.html', context)

def home(request):
    return render(request, 'law/home.html')

def about(request):
    return render(request, 'law/about.html')

def services(request):
    return render(request, 'law/services.html')

def contact(request):
    form = ContactsViewModelForm()
    if request.method == 'POST':
        form = ContactsViewModelForm(request.POST)
        if form.is_valid():
            form.save()
            # Form başarıyla gönderildikten sonra aynı sayfaya yönlendir
            return redirect('law:contact')  # 'contact' URL adını urlpatterns'ten kontrol edin
    return render(request, 'law/contact.html', {'form': form})

def team(request):
    return render(request, 'law/team.html')

def success_stories(request):
    context = {
        'stories': SUCCESS_STORIES
    }
    return render(request, 'law/success_stories.html', context)

def faq(request):
    context = {
        'faq_items': FAQ_ITEMS
    }
    return render(request, 'law/faq.html', context)

def legal_notice(request):
    return render(request, 'law/legal_notice.html')

@api_view(['GET', 'POST'])
def contact_api(request):
    if request.method == 'GET':
        # Tüm veriyi serialize ederek döndür
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Gelen veriyi deseralize ederek kaydet
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)