# Job Application Coach

A Claude skill that takes a candidate through a single job application, end to end. Never invents experience.
İş başvurusunu baştan sona yöneten bir Claude skill'i. Asla deneyim uydurmaz.

**[English](#english) · [Türkçe](#türkçe)**

---

## English

A Claude skill that takes a candidate through a single job application, end to end:

1. Intake of the CV and a detailed career narrative
2. Company and role research
3. Fit report with an apply / apply light / do not apply decision
4. Gap strategy that never invents experience
5. Two tailored CVs: the candidate's own file edited in place, and a professional ATS-safe template
6. A one-page cover letter in the candidate's voice
7. Profile alignment on every job platform (professional networks, job boards, company career portals), consistent with all open applications
8. Pre-send check for hidden text, watermarks, metadata, tracking IDs and generic phrasing
9. Recruiter and network outreach messages
10. Interview preparation, one-way video interviews and salary method
11. Follow-up timing, reading signals and rejection replies

### Principles

- Nothing goes into a CV, letter or answer that the candidate does not have.
- Every number comes from the candidate.
- Text should sound like the candidate and be specific enough to defend in an interview.
- Titles and dates stay consistent across the CV, every job-platform profile and every open application.

### Contents

```
job-application-coach/
  SKILL.md                     workflow and rules
  assets/cv-template.docx      ATS-safe CV template
  scripts/docx_tools.py        edit a .docx in place without breaking formatting
  scripts/docx_check.py        hidden content, metadata, ATS and writing-signal check
  scripts/keyword_gap.py       posting terms missing from the CV
  references/                  intake questions, fit report, writing rules,
                               job-platform profiles and outreach, interview prep, after applying
```

### Install

#### Claude app (web and desktop)

1. Download **`job-application-coach.zip` from the [Releases](../../releases) page** of this repository.
   Do not use GitHub's green "Code > Download ZIP" button: it wraps the files in an extra folder
   (`repo-name-main/...`) and Claude will reject the upload because the folder name no longer
   matches the skill name.
2. In Claude, open **Settings > Capabilities** and turn on **Code execution and file creation**
   (shown as "Create and edit files" in newer layouts). The skill needs it to edit Word files and run its checks.
3. Go to **Customize > Skills**, click **+**, then **+ Create skill**, then **Upload a skill**.
4. Select the ZIP. The skill appears in your list; make sure its toggle is on.

On Team and Enterprise plans, an organisation owner must allow user-created skills and code execution.
Official guide: [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

#### Claude Code

Copy the `job-application-coach` folder (the one that contains `SKILL.md`) to:

- `~/.claude/skills/job-application-coach/` to use it in all your projects, or
- `.claude/skills/job-application-coach/` inside a repository to share it with everyone working there.

Official guide: [Skills in Claude Code](https://code.claude.com/docs/en/skills).

#### Using it

No special command is needed. Claude loads the skill whenever a request is about a job application,
in any language. Attach your CV and paste the job posting, then ask in your own words, for example:

- "I want to apply for this job. Is it a good fit for me?"
- "Tailor my CV and write a cover letter for this posting."

It also works for single steps:

- "Check my cover letter before I send it."
- "Prepare me for the interview at this company."
- "How should I reply to this rejection?"

If Claude does not pick it up, name it directly: "Use the job-application-coach skill."
In Claude Code you can also type `/job-application-coach`.

#### Requirements for the scripts

Python 3 and `python-docx`. Claude's code execution environment usually has it; locally:

```
pip install python-docx
```

### Quick script examples

```
python scripts/docx_tools.py my_cv.docx --dump
python scripts/docx_tools.py my_cv.docx tailored.docx edits.json
python scripts/keyword_gap.py posting.txt tailored.docx --terms "term one, term two"
python scripts/docx_check.py tailored.docx cover_letter.docx
```

### Privacy

The skill works with personal data. It instructs Claude to use that data only inside the conversation and not to store it anywhere unless the user asks.

### Disclaimer

Salary, contract and tax guidance is general information, not legal or tax advice.

### License

Copyright (c) 2026 Serdar Sevindi.
Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [LICENSE](LICENSE).

- **Free for personal use**: use it for your own job search, adapt it, share it with friends.
- **Not for commercial use**: do not sell it, put it in a paid product, or use it to deliver paid services such as paid career coaching.
- **Credit and share alike**: if you share it or a modified version, credit Serdar Sevindi, link to this repository and the license, and release your version under the same license.

If you would like to use it in a way the license does not allow, ask first.

### For the repository owner: publishing a release

Upload `job-application-coach.zip` as a release asset (Releases > Draft a new release > attach the file).
The ZIP must contain a single top-level folder named `job-application-coach` with `SKILL.md` directly inside it.
To rebuild it from the repository:

```
zip -r job-application-coach.zip job-application-coach -x "*/__pycache__/*"
```

---

## Türkçe

Bir adayı tek bir iş başvurusunda baştan sona yönlendiren bir Claude skill'i:

1. CV'nin ve ayrıntılı kariyer hikayesinin toplanması
2. Şirket ve pozisyon araştırması
3. "Başvur / az emekle başvur / başvurma" kararıyla biten uyum raporu
4. Asla deneyim uydurmayan bir açık kapatma stratejisi
5. İki uyarlanmış CV: adayın kendi dosyası (biçimi bozulmadan düzenlenmiş) ve profesyonel, ATS uyumlu bir şablon
6. Adayın kendi sesiyle yazılmış, tek sayfalık ön yazı (cover letter)
7. Tüm iş platformlarında (profesyonel ağlar, ilan siteleri, şirket kariyer portalları) açık başvurularla tutarlı profil uyumu
8. Göndermeden önce gizli metin, filigran, meta veri, izleme kimlikleri ve kalıp ifadeler için kontrol
9. İK uzmanına ve eski çalışma arkadaşlarına mesajlar
10. Mülakat hazırlığı, tek yönlü video mülakatlar ve maaş beklentisi yöntemi
11. Takip zamanlaması, sinyalleri okuma ve ret maillerine cevap

### İlkeler

- Adayda olmayan hiçbir şey CV'ye, ön yazıya ya da mülakat cevabına girmez.
- Her rakam adaydan gelir.
- Metin adayın kendisi gibi konuşmalı ve mülakatta savunulabilecek kadar somut olmalı.
- Unvanlar ve tarihler CV'de, tüm iş platformu profillerinde ve açık başvuruların hepsinde aynı kalır.

### İçerik

```
job-application-coach/
  SKILL.md                     iş akışı ve kurallar
  assets/cv-template.docx      ATS uyumlu CV şablonu
  scripts/docx_tools.py        bir .docx dosyasını biçimini bozmadan düzenler
  scripts/docx_check.py        gizli içerik, meta veri, ATS ve yazım kalıbı kontrolü
  scripts/keyword_gap.py       ilanda geçip CV'de geçmeyen terimler
  references/                  giriş soruları, uyum raporu, yazım kuralları,
                               iş platformu profilleri ve mesajlar, mülakat hazırlığı, başvuru sonrası
```

### Kurulum

#### Claude uygulaması (web ve masaüstü)

1. Bu deponun **[Releases](../../releases) sayfasından `job-application-coach.zip`** dosyasını indirin.
   GitHub'ın yeşil "Code > Download ZIP" düğmesini kullanmayın: dosyaları fazladan bir klasörün içine
   koyar (`depo-adi-main/...`) ve klasör adı skill adıyla eşleşmediği için Claude yüklemeyi reddeder.
2. Claude'da **Settings > Capabilities** bölümünü açın ve **Code execution and file creation** ayarını açın
   (yeni düzende "Create and edit files" olarak görünür). Skill, Word dosyalarını düzenlemek ve
   kontrollerini çalıştırmak için bu ayara ihtiyaç duyar.
3. **Customize > Skills** bölümüne gidin; **+**, ardından **+ Create skill**, ardından **Upload a skill** seçin.
4. ZIP dosyasını seçin. Skill listenizde görünür; açık olduğundan emin olun.

Claude'un arayüz dili Türkçeyse menü adları Türkçe görünebilir.
Team ve Enterprise planlarında, kullanıcıların skill yüklemesine ve kod çalıştırmasına kuruluş yöneticisinin izin vermesi gerekir.
Resmi rehber: [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

#### Claude Code

`SKILL.md` dosyasını içeren `job-application-coach` klasörünü şuraya kopyalayın:

- Tüm projelerinizde kullanmak için `~/.claude/skills/job-application-coach/`
- Bir depoda çalışan herkesle paylaşmak için o deponun içinde `.claude/skills/job-application-coach/`

Resmi rehber: [Skills in Claude Code](https://code.claude.com/docs/en/skills).

#### Kullanım

Özel bir komut gerekmez. İsteğiniz bir iş başvurusuyla ilgili olduğunda Claude skill'i kendiliğinden kullanır;
hangi dilde yazdığınız fark etmez. CV'nizi ekleyin, ilan metnini yapıştırın ve kendi cümlelerinizle sorun, örneğin:

- "Bu ilana başvurmak istiyorum. Bana uygun mu?"
- "CV'mi bu ilana göre düzenle ve bir ön yazı yaz."

Tek adımlık işler için de çalışır:

- "Ön yazımı göndermeden önce kontrol et."
- "Bu şirketteki mülakata beni hazırla."
- "Bu ret mailine nasıl cevap vereyim?"

Claude skill'i kullanmazsa adıyla isteyin: "job-application-coach skill'ini kullan."
Claude Code'da `/job-application-coach` da yazabilirsiniz.

#### Betikler için gereksinimler

Python 3 ve `python-docx`. Claude'un kod çalıştırma ortamında genelde yüklüdür; kendi bilgisayarınızda:

```
pip install python-docx
```

### Hızlı betik örnekleri

```
python scripts/docx_tools.py cv.docx --dump
python scripts/docx_tools.py cv.docx uyarlanmis_cv.docx duzenlemeler.json
python scripts/keyword_gap.py ilan.txt uyarlanmis_cv.docx --terms "terim bir, terim iki"
python scripts/docx_check.py uyarlanmis_cv.docx on_yazi.docx
```

### Gizlilik

Skill kişisel verilerle çalışır. Claude'a bu verileri yalnızca sohbetin içinde kullanmasını ve kullanıcı istemedikçe hiçbir yere kaydetmemesini söyler.

### Sorumluluk reddi

Maaş, sözleşme ve vergi konusundaki yönlendirmeler genel bilgidir; hukuki ya da vergi danışmanlığı değildir.

### Lisans

Telif hakkı (c) 2026 Serdar Sevindi.
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.tr) lisansıyla lisanslanmıştır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın; bağlayıcı olan, lisansın resmi metnidir.

- **Kişisel kullanım serbest:** Kendi iş aramanızda kullanın, uyarlayın, arkadaşlarınızla paylaşın.
- **Ticari kullanım yasak:** Satmayın, ücretli bir ürüne koymayın, ücretli kariyer danışmanlığı gibi ücretli hizmetlerde kullanmayın.
- **Atıf ve aynı lisansla paylaşım:** Paylaştığınızda ya da değiştirdiğiniz bir sürümünü yayınladığınızda Serdar Sevindi'yi belirtin, bu depoya ve lisansa bağlantı verin ve sürümünüzü aynı lisansla yayınlayın.

Lisansın izin vermediği bir şekilde kullanmak isterseniz önce sorun.
