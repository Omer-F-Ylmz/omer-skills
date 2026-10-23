# scroll-trigger-animasyon (DebtKK3DrMQ)

**Amaç:** Scroll ile tetiklenen animasyonlar oluşturmak.
**Araçlar:** GSAP (GreenSock Animation Platform), ScrollTrigger (GSAP plugin), Flip (GSAP plugin), Draggable (GSAP plugin), MotionPathPlugin (GSAP plugin)

**Adımlar**
1. [] GSAP kütüphanesini ve gerekli plugin'leri (ScrollTrigger, Flip, Draggable, MotionPathPlugin) import edin.
2. [] ScrollTrigger'ı kullanarak scroll ile tetiklenen animasyon timelines'ını oluşturun.
3. [] Flip plugin'ini kullanarak performanslı animasyonlar (morphing, text splitting) oluşturun.
4. [] MotionPathPlugin ile nesnelerin hareket yollarını animasyon haline getirin.

**Prompt/kod/ayar:** import gsap from 'gsap'; import ScrollTrigger from 'gsap/ScrollTrigger'; gsap.registerPlugin(ScrollTrigger);
**Sonuç:** Scroll ile tetiklenen animasyonlar oluşturulur ve kullanıcıya daha dinamik bir deneyim sunulur.
**Bizde (öneri, modelden):** GSAP ve ScrollTrigger'ı kullanarak scroll-driven animasyonlar oluşturabilirsiniz. Flip, Draggable gibi plugin'leri entegre ederek daha karmaşık etkiler elde edebilirsiniz.
**Daha iyi (öneri):** GSAP'ın performans avantajlarından yararlanarak, browser inconsistency'lerini aşarak daha hızlı ve güvenilir animasyonlar oluşturun.
